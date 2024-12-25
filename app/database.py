from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/w1_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
from .models import User
from .models import Session
from .models import CalendarEvent
from .models import Product
from .models import Order
from .models import Expense

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
