from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from api import schemas, crud
from api.database import get_db
from api.auth import get_current_user

router = APIRouter()


def _get_customer_portal_result(db: Session, customer_id: str, from_date: Optional[str], to_date: Optional[str]):
    result = crud.get_customer_portal(db, customer_id, from_date=from_date, to_date=to_date)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result

@router.get("/", response_model=schemas.CustomerPortalResponse)
def customer_portal_query(
    customer_id: str = Query(..., alias="customer_id"),
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return _get_customer_portal_result(db, customer_id, from_date, to_date)

@router.get("/{customer_id}", response_model=schemas.CustomerPortalResponse)
def customer_portal(
    customer_id: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return _get_customer_portal_result(db, customer_id, from_date, to_date)
