from tkinter import Image
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
import requests
from io import BytesIO
from transformers import LLaVAModel, LLaVATokenizer


router = APIRouter()

# Load the LLaVA model and tokenizer
model_name = "huggingface/llava"
model = LLaVAModel.from_pretrained(model_name)
tokenizer = LLaVATokenizer.from_pretrained(model_name)

def get_relevant_products(description: str) -> List[dict]:
    # Replace with the actual URL of the HashCart product search API
    hashcart_api_url = "http://localhost:8000/api/products/search"
    response = requests.post(hashcart_api_url, json={"query": description})
    response.raise_for_status()
    return response.json()

@router.post("/search")
async def search_product(image: UploadFile = File(...)):
    try:
        # Read the image
        image_data = await image.read()
        image = Image.open(BytesIO(image_data))

        # Preprocess the image
        inputs = tokenizer(images=image, return_tensors="pt")

        # Generate description using the LLaVA model
        outputs = model.generate(**inputs)
        description = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Fetch relevant products from HashCart
        products = get_relevant_products(description)
        return {"description": description, "products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

