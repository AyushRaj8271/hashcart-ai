from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict

class UserBase(BaseModel):
    name: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class SessionCreate(BaseModel):
    user_id: int

class Session(BaseModel):
    id: int
    user_id: int
    context: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    currency: str
    brand: str
    category: str
    stock_quantity: int
    average_rating: float
    total_reviews: int
    specifications: Dict[str, str]
    

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    currency: str
    brand: str
    category: str
    stock_quantity: int
    average_rating: float
    total_reviews: int
    specifications: Dict[str, str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CalendarEventCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    reminder_time: Optional[datetime]

class CalendarEvent(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    reminder_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# class ExpenseCreate(BaseModel):
#     user_id: int
#     amount: float
#     category: str
#     description: Optional[str]

# class Expense(BaseModel):
#     id: int
#     user_id: int
#     amount: float
#     category: str
#     description: Optional[str]
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         orm_mode = True
class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: str
    created_at: datetime
    updated_at: datetime

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    

class CreateSessionResponse(BaseModel):
    session_id: int

class FetchSessionsResponse(BaseModel):
    sessions: list

class GetSessionHistoryResponse(BaseModel):
    history: list

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    response: str
    
    