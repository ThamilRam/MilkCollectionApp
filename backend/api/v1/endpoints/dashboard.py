from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from api import schemas, crud
from api.database import get_db
from api.auth import get_current_user

router = APIRouter()

@router.get("/summary", response_model=schemas.DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_dashboard_summary(db)

@router.get("/date-wise", response_model=List[schemas.DateWiseSummary])
def date_wise(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
):
    results = crud.get_date_wise_summary(db, from_date=from_date, to_date=to_date)
    return [schemas.DateWiseSummary(
        date=r.date,
        total_milk=r.total_milk,
        total_amount=r.total_amount,
        am_count=r.am_count,
        pm_count=r.pm_count,
        am_milk=r.am_milk,
        pm_milk=r.pm_milk
    ) for r in results]


@router.get("/customer-monthly", response_model=List[schemas.CustomerMonthlyMilkSummary])
def customer_monthly(
    customer_id: str,
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    current_year = year or date.today().year
    results = crud.get_customer_monthly_milk_summary(db, customer_id, current_year)
    return [schemas.CustomerMonthlyMilkSummary(month=int(r.month), total_milk=r.total_milk) for r in results]


@router.get("/top-customers", response_model=List[schemas.TopCustomerMonthSummary])
def top_customers(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    today = date.today()
    if month is None:
        selected_month = today.month - 1 or 12
    else:
        selected_month = month
    selected_year = year or today.year
    if today.month == 1 and month is None:
        selected_year = today.year - 1
    results = crud.get_top_customers_by_month(db, selected_year, selected_month)
    return [schemas.TopCustomerMonthSummary(
        customer_id=r.customer_id,
        customer_name=r.customer_name,
        total_milk=r.total_milk
    ) for r in results]