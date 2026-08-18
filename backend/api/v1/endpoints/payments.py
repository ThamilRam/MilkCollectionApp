from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from api import schemas, crud
from api.database import get_db
from api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.PaymentRecordResponse])
def read_payments(customer_id: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_payments(db, customer_id=customer_id)

@router.post("/", response_model=schemas.PaymentRecordResponse, status_code=201)
def create_payment(payment: schemas.PaymentRecordCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.create_payment(db, payment)

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    payment = crud.delete_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")
    return {"message": "Payment record deleted"}