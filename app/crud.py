from sqlalchemy.orm import Session
from app import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_session(db: Session, session: schemas.SessionCreate):
    db_session = models.Session(user_id=session.user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_sessions(db: Session, user_id: int):
    return db.query(models.Session).filter(models.Session.user_id == user_id).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        currency=product.currency,
        brand=product.brand,
        category=product.category,
        stock_quantity=product.stock_quantity,
        average_rating=product.average_rating,
        total_reviews=product.total_reviews,
        specifications=product.specifications,
        embedding=product.embedding # Add the embedding field
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_event(db: Session, event_id: int):
    return db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.CalendarEvent).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.CalendarEventCreate):
    db_event = models.CalendarEvent(
        user_id=event.user_id,
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        reminder_time=event.reminder_time
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event: schemas.CalendarEventCreate):
    db_event = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if db_event:
        db_event.title = event.title
        db_event.description = event.description
        db_event.start_time = event.start_time
        db_event.end_time = event.end_time
        db_event.reminder_time = event.reminder_time
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event


def get_product(db: Session, product_id: int) -> schemas.Product:
    """
    Fetch a product by its ID from the database.
    
    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to fetch.
    
    Returns:
        schemas.Product: The product schema object.
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None
    return schemas.Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        currency=product.currency,
        brand=product.brand,
        category=product.category,
        stock_quantity=product.stock_quantity,
        average_rating=product.average_rating,
        total_reviews=product.total_reviews,
        specifications=product.specifications,
        created_at=product.created_at,
        updated_at=product.updated_at
    )
    
    
def get_orders(db: Session, query: str):
    return db.query(models.Order).filter(models.Order.product_name.contains(query)).all()

    
def get_products(db: Session, query: str):
    return db.query(models.Product).filter(models.Product.name.contains(query)).all()

def get_expenses(db: Session, query: str):
    return db.query(models.Expense).filter(models.Expense.description.contains(query)).all()


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()