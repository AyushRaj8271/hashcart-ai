# app/routers/expenses.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, dependencies, models, utils
from sqlalchemy import create_engine
from app.models import Base, Expense
import csv
import io
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from app.database import get_db
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

router = APIRouter()

@router.get("/api/expenses/report", response_class=StreamingResponse)
def generate_expense_report(db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.shopper_access)):
    expenses = db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()
    
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found")

    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write CSV header
    writer.writerow(["ID", "User ID", "Amount", "Category", "Description", "Created At", "Updated At"])
    
    # Write expense data
    for expense in expenses:
        writer.writerow([expense.id, expense.user_id, expense.amount, expense.category, expense.description, expense.created_at, expense.updated_at])
    
    output.seek(0)
    
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=expense_report.csv"})


@router.post("/api/expenses/", response_model=schemas.Expense)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    db_expense = models.Expense(
        user_id=current_user.id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        created_at=expense.created_at,
        updated_at=expense.updated_at
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/expenses/")
def read_expenses(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).offset(skip).limit(limit).all()
    return expenses

@router.get("/expenses/{expense_id}")
def read_expense(expense_id: int, user_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.get("/expenses/csv/")
def export_expenses_to_csv(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    df = pd.DataFrame([{
        "id": expense.id,
        "user_id": expense.user_id,
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description,
        "created_at": expense.created_at,
        "updated_at": expense.updated_at
    } for expense in expenses])
    csv_file = "expenses.csv"
    df.to_csv(csv_file, index=False)
    return FileResponse(csv_file, media_type='text/csv', filename=csv_file)

@router.get("/expenses/visualize/")
def visualize_expenses(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    df = pd.DataFrame([{
        "id": expense.id,
        "user_id": expense.user_id,
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description,
        "created_at": expense.created_at,
        "updated_at": expense.updated_at
    } for expense in expenses])
    
    # Plotting
    plt.figure(figsize=(10, 6))
    sns.barplot(x="category", y="amount", data=df, estimator=sum)
    plt.title("Total Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("expenses_by_category.png")
    
    return FileResponse("expenses_by_category.png", media_type='image/png', filename="expenses_by_category.png")

@router.get("/expenses/advice/")
def financial_advice(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    df = pd.DataFrame([{
        "id": expense.id,
        "user_id": expense.user_id,
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description,
        "created_at": expense.created_at,
        "updated_at": expense.updated_at
    } for expense in expenses])
    
    # Example recommendation logic
    advice = []
    total_expense = df['amount'].sum()
    if total_expense > 1000:  # Example threshold
        advice.append("Your total expenses are quite high. Consider reducing discretionary spending.")
    
    category_expenses = df.groupby('category')['amount'].sum()
    for category, amount in category_expenses.items():
        if amount > 500:  # Example threshold
            advice.append(f"Consider reducing expenses in the {category} category.")
    
    return {"advice": advice}