from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api import schemas, crud
from api.database import get_db
from api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.PurchaseResponse])
def read_purchases(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not crud.get_customer(db, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.get_purchases(db, customer_id)

@router.post("/", response_model=schemas.PurchaseResponse, status_code=201)
def create_purchase(
    purchase: schemas.PurchaseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_purchase, error = crud.create_purchase(db, purchase)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return db_purchase

@router.patch("/{purchase_id}", response_model=schemas.PurchaseResponse)
def update_purchase_paid(
    purchase_id: int,
    update: schemas.PurchasePaidUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    purchase = crud.update_purchase_paid(db, purchase_id, update.paid)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

@router.delete("/{purchase_id}")
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    purchase = crud.delete_purchase(db, purchase_id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return {"message": "Purchase deleted"}
