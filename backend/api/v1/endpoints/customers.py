from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api import schemas, crud
from api.database import get_db
from api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.CustomerResponse])
def read_customers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 1000
):
    return crud.get_customers(db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=schemas.CustomerResponse)
def read_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=schemas.CustomerResponse, status_code=201)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_customer(db, customer)

@router.put("/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer(
    customer_id: str,
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_customer = crud.update_customer(db, customer_id, customer)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_customer = crud.delete_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}