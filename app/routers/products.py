
from langchain_groq import ChatGroq
import psycopg2
import numpy as np
from fastapi import APIRouter, Depends, HTTPException,File,UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import schemas, dependencies, models, utils,crud
from langchain_huggingface import HuggingFaceEmbeddings
import datetime
import json
import ast
import io
import datetime
from app.database import get_db
from transformers import pipeline
import pymupdf 
import fitz
from typing import List

router = APIRouter()


embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db_connection = {
    "dbname": "w1_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def cosine_similarity(vec1, vec2):
    """Calculate the cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

@router.post("/api/products/upload", response_model=schemas.Product)
async def upload_product(product: schemas.ProductCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.shopper_access)):
    print("Current user role in route:", current_user.role) 
    # Generate embedding for the product
    texter = product.name + " " + product.description
    product_embedding = embeddings_model.embed_query(texter)

    # Convert specifications dictionary to JSON string
    specifications_json = json.dumps(product.specifications)

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_connection)
    cur = conn.cursor()

    try:
        # Insert product data into the database
        cur.execute("""
            INSERT INTO products (
                name, description, price, currency, brand, category, stock_quantity, average_rating, total_reviews,
                specifications, created_at, updated_at, embedding
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, name, description, price, currency, brand, category, stock_quantity, average_rating, total_reviews,
                specifications, created_at, updated_at, embedding
        """, (
            product.name, product.description, product.price, product.currency, product.brand,
            product.category, product.stock_quantity, product.average_rating, product.total_reviews,
            specifications_json, datetime.datetime.utcnow(), datetime.datetime.utcnow(), product_embedding
        ))

        # Fetch the inserted product to return as a response
        inserted_product = cur.fetchone()

        if not inserted_product:
            raise HTTPException(status_code=404, detail="Product not found after insertion")

        # Commit the transaction
        conn.commit()

        # Convert the fetched product to a dictionary
        product_dict = {
            "id": inserted_product[0],
            "name": inserted_product[1],
            "description": inserted_product[2],
            "price": inserted_product[3],
            "currency": inserted_product[4],
            "brand": inserted_product[5],
            "category": inserted_product[6],
            "stock_quantity": inserted_product[7],
            "average_rating": inserted_product[8],
            "total_reviews": inserted_product[9],
            "specifications": str(json.loads(inserted_product[10])),  # Convert JSON string back to dictionary
            "created_at": inserted_product[11],
            "updated_at": inserted_product[12],
            "embedding": inserted_product[13]
        }
        
        print("dict--- ",product_dict)
        return JSONResponse(content=product_dict)

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()

@router.post("/search/", response_model=List[schemas.Product])
def search_products(query: str, db: Session = Depends(dependencies.get_db)):
    query_embedding = embeddings_model.embed_query(query)

    conn = psycopg2.connect(**db_connection)
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, embedding FROM products")
        products = cur.fetchall()

        similarities = []
        for product in products:
            product_id, product_embedding = product

            # Check if the product embedding is None
            if product_embedding is None:
                continue

            # Convert the embedding from JSON string back to a numpy array
            product_embedding = np.array(json.loads(product_embedding))

            # Calculate cosine similarity
            similarity = np.dot(query_embedding, product_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(product_embedding))
            similarities.append((product_id, similarity))

        # Sort products by similarity score in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Get the top 10 product IDs
        top_product_ids = [product_id for product_id, similarity in similarities[:10]]

        # Fetch the top products from the database
        top_products = [crud.get_product(db, product_id=product_id) for product_id in top_product_ids]

        return top_products

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()