from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api import schemas, crud
from api.database import get_db
from api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ProductResponse])
def read_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 1000
):
    return crud.get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas.ProductResponse, status_code=201)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_product(db, product)

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_product = crud.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_product = crud.delete_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
