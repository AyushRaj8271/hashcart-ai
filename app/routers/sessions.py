from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, dependencies
from typing import List

router = APIRouter()

@router.post("/create-session", response_model=schemas.Session)
def create_session(session: schemas.SessionCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_session(db=db, session=session)

@router.get("/fetch-sessions", response_model=List[schemas.Session])
def fetch_sessions(user_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.get_sessions(db=db, user_id=user_id)