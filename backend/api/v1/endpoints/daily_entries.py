from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from api import schemas, crud
from api.database import get_db
from api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.DailyEntryResponse])
def read_entries(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    customer_id: Optional[str] = None,
    session: Optional[str] = None,
    skip: int = 0,
    limit: int = 50000
):
    return crud.get_entries(db, from_date=from_date, to_date=to_date, customer_id=customer_id, session=session, skip=skip, limit=limit)

@router.post("/", response_model=schemas.DailyEntryResponse, status_code=201)
def create_entry(entry: schemas.DailyEntryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.create_entry(db, entry)

@router.post("/bulk", status_code=201)
def create_bulk(entries: List[schemas.DailyEntryCreate], db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    count = crud.create_entries_bulk(db, entries)
    return {"message": f"{count} entries created"}

@router.delete("/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = crud.delete_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"message": "Entry deleted"}