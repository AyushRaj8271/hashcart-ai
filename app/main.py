from fastapi import FastAPI
from app.database import engine, Base
from .routers import products,calendar,users,auth,expenses,orders,chat,sessions
import logging

logging.basicConfig(level=logging.INFO)

app.logger.info("Application started")

app = FastAPI()

app.include_router(products.router, tags=["Products"])

app.include_router(calendar.router, tags=["Events"])
app.include_router(users.router, tags=["Users"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(expenses.router, tags=["Expenses"])
app.include_router(orders.router,tags=["orders"])
app.include_router(chat.router,tags=["chat"])
app.include_router(sessions.router,tags=["sessions"])
# app.include_router(product_img.router,tags=["product-img"])