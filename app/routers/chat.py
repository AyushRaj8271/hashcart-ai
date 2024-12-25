from fastapi import APIRouter, FastAPI, HTTPException, Depends
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import Dict

load_dotenv()

router = APIRouter()

groq_api_key = os.getenv("GROQ_API_KEY")
auth_token = os.getenv("AUTH_TOKEN")

headers = {
    "Authorization": f"Bearer {auth_token}"
}

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    response: str

def get_orders(query: str):
    response = requests.post(f"http://localhost:8000/api/orders/search", json={"query": query}, headers=headers)
    return response.json()

def get_products(query: str):
    response = requests.post(f"http://localhost:8000/search/?query={query}", headers=headers)
    return response.json()

def get_expenses(query: str):
    response = requests.get(f"http://localhost:8000/expenses/?user_id=5&skip=0&limit=10", headers=headers)
    return response.json()

def get_events(query: str):
    response = requests.get(f"http://localhost:8000/events/?skip=1&limit=10", headers=headers)
    return response.json()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # Call the Groq API with the user question
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {groq_api_key}"},
            json={"question": request.question}
        )
        response.raise_for_status()
        groq_response = response.json()

        # Analyze the intent and call specific API endpoints
        intent = groq_response['response']
        print("Intent:", intent)

        if "expenses" in intent or "expenses" in request.question:
            expenses = get_expenses(request.question)
            response_text = f"Expenses: {expenses}"
        elif "meeting" in intent or "event" in intent or "meetings" in request.question or "event" in request.question:
            events = get_events(request.question)
            response_text = f"Events: {events}"
        elif "product" in intent or "products" in request.question:
            products = get_products(request.question)
            response_text = f"Products: {products}"
        elif "order" in intent or "order" in request.question:
            orders = get_orders(request.question)
            response_text = f"Orders: {orders}"
        else:
            response_text = groq_response['response']

        return {"response": response_text}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

