
import token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, dependencies,roles,models

router = APIRouter()

@router.post("/events/", response_model=schemas.CalendarEvent)
def create_event(event: schemas.CalendarEventCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.business_access)):
#def create_event(event: schemas.CalendarEventCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_event(db=db, event=event)

@router.get("/events/", response_model=list[schemas.CalendarEvent])
#def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.business_access)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events

@router.get("/events/{event_id}", response_model=schemas.CalendarEvent)
def read_event(event_id: int, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.business_access)):
#def read_event(event_id: int, db: Session = Depends(dependencies.get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

# @router.put("/events/{event_id}", response_model=schemas.CalendarEvent)
# def update_event(event_id: int, event: schemas.CalendarEventUpdate, db: Session = Depends(dependencies.get_db)):
#     db_event = crud.update_event(db, event_id=event_id, event=event)
#     if db_event is None:
#         raise HTTPException(status_code=404, detail="Event not found")
#     return db_event

@router.delete("/events/{event_id}", response_model=schemas.CalendarEvent)
def delete_event(event_id: int, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.business_access)):
# def delete_event(event_id: int, db: Session = Depends(dependencies.get_db)):
    db_event = crud.delete_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

def test_get_access_permission():
    access_permission_func = dependencies.get_access_permission(roles.Accesses.CALENDAR)
    print(access_permission_func)