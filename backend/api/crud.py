from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case, desc
from decimal import Decimal
from datetime import date
from typing import Optional, List
from api import models, schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_customers(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def get_customer(db: Session, customer_id: str):
    return db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: str, customer: schemas.CustomerCreate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: str):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()
    return db_customer

def get_products(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Product).order_by(models.Product.product_name).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    return db_product

def get_purchases(db: Session, customer_id: str):
    return db.query(models.PurchaseRecord).filter(
        models.PurchaseRecord.customer_id == customer_id
    ).order_by(models.PurchaseRecord.created_at.desc()).all()

def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    customer = get_customer(db, purchase.customer_id)
    product = get_product(db, purchase.product_id)
    if not customer or not product:
        return None, "Customer or product not found"
    if not product.active:
        return None, "Product is inactive"
    if purchase.quantity > product.quantity:
        return None, "Purchase quantity exceeds available quantity"

    db_purchase = models.PurchaseRecord(
        customer_id=purchase.customer_id,
        product_id=purchase.product_id,
        quantity=purchase.quantity,
        unit_price=product.price,
        amount=purchase.quantity * product.price,
        paid=purchase.paid,
    )
    product.quantity -= purchase.quantity
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase, None

def update_purchase_paid(db: Session, purchase_id: int, paid: bool):
    purchase = db.query(models.PurchaseRecord).filter(models.PurchaseRecord.id == purchase_id).first()
    if not purchase:
        return None
    purchase.paid = paid
    db.commit()
    db.refresh(purchase)
    return purchase

def delete_purchase(db: Session, purchase_id: int):
    purchase = db.query(models.PurchaseRecord).filter(models.PurchaseRecord.id == purchase_id).first()
    if not purchase:
        return None
    product = get_product(db, purchase.product_id)
    if product:
        product.quantity += purchase.quantity
    db.delete(purchase)
    db.commit()
    return purchase

def get_entries(db: Session, from_date=None, to_date=None, customer_id=None, session=None, skip=0, limit=50000):
    query = db.query(models.DailyEntry)
    if from_date:
        query = query.filter(models.DailyEntry.date >= from_date)
    if to_date:
        query = query.filter(models.DailyEntry.date <= to_date)
    if customer_id:
        query = query.filter(models.DailyEntry.customer_id == customer_id)
    if session:
        query = query.filter(models.DailyEntry.session == session)
    return query.order_by(models.DailyEntry.date.desc(), models.DailyEntry.session.desc()).offset(skip).limit(limit).all()

def create_entry(db: Session, entry: schemas.DailyEntryCreate):
    calc = entry.quantity * entry.rate
    if entry.amount != calc:
        entry.amount = calc
    db_entry = models.DailyEntry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def create_entries_bulk(db: Session, entries: List[schemas.DailyEntryCreate]):
    db_entries = []
    for entry in entries:
        data = entry.model_dump()
        data['amount'] = entry.quantity * entry.rate
        db_entries.append(models.DailyEntry(**data))
    db.add_all(db_entries)
    db.commit()
    return len(db_entries)

def delete_entry(db: Session, entry_id: int):
    entry = db.query(models.DailyEntry).filter(models.DailyEntry.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return entry

def get_payments(db: Session, customer_id: Optional[str] = None):
    query = db.query(models.PaymentRecord)
    if customer_id:
        query = query.filter(models.PaymentRecord.customer_id == customer_id)
    return query.order_by(models.PaymentRecord.from_date.desc()).all()

def create_payment(db: Session, payment: schemas.PaymentRecordCreate):
    db_payment = models.PaymentRecord(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, payment_id: int):
    payment = db.query(models.PaymentRecord).filter(models.PaymentRecord.id == payment_id).first()
    if payment:
        db.delete(payment)
        db.commit()
    return payment

def get_dashboard_summary(db: Session):
    today = date.today()
    active_customers = db.query(models.Customer).filter(models.Customer.status == "Active").count()
    today_result = db.query(
        func.coalesce(func.sum(models.DailyEntry.quantity), 0).label("milk"),
        func.coalesce(func.sum(models.DailyEntry.amount), 0).label("amount")
    ).filter(models.DailyEntry.date == today).first()
    month_result = db.query(
        func.coalesce(func.sum(models.DailyEntry.quantity), 0).label("milk"),
        func.coalesce(func.sum(models.DailyEntry.amount), 0).label("amount")
    ).filter(
        extract('year', models.DailyEntry.date) == today.year,
        extract('month', models.DailyEntry.date) == today.month
    ).first()
    total_result = db.query(
        func.coalesce(func.sum(models.DailyEntry.quantity), 0).label("milk"),
        func.coalesce(func.sum(models.DailyEntry.amount), 0).label("amount")
    ).first()
    return {
        "active_customers": active_customers,
        "today_milk": today_result.milk,
        "today_amount": today_result.amount,
        "month_milk": month_result.milk,
        "month_amount": month_result.amount,
        "total_milk": total_result.milk,
        "total_amount": total_result.amount,
        "today_date": today
    }

def get_date_wise_summary(db: Session, from_date=None, to_date=None):
    query = db.query(
        models.DailyEntry.date,
        func.sum(models.DailyEntry.quantity).label("total_milk"),
        func.sum(models.DailyEntry.amount).label("total_amount"),
        func.sum(case((models.DailyEntry.session == "AM", 1), else_=0)).label("am_count"),
        func.sum(case((models.DailyEntry.session == "PM", 1), else_=0)).label("pm_count"),
        func.sum(case((models.DailyEntry.session == "AM", models.DailyEntry.quantity), else_=0)).label("am_milk"),
        func.sum(case((models.DailyEntry.session == "PM", models.DailyEntry.quantity), else_=0)).label("pm_milk")
    ).group_by(models.DailyEntry.date)
    if from_date:
        query = query.filter(models.DailyEntry.date >= from_date)
    if to_date:
        query = query.filter(models.DailyEntry.date <= to_date)
    results = query.order_by(models.DailyEntry.date.desc()).all()
    return results


def get_customer_monthly_milk_summary(db: Session, customer_id: str, year: int):
    query = db.query(
        extract('month', models.DailyEntry.date).label('month'),
        func.coalesce(func.sum(models.DailyEntry.quantity), 0).label('total_milk')
    ).filter(
        models.DailyEntry.customer_id == customer_id,
        extract('year', models.DailyEntry.date) == year
    ).group_by(extract('month', models.DailyEntry.date)).order_by(extract('month', models.DailyEntry.date))
    return query.all()


def get_top_customers_by_month(db: Session, year: int, month: int, count: int = 3):
    query = db.query(
        models.DailyEntry.customer_id,
        models.Customer.name.label('customer_name'),
        func.coalesce(func.sum(models.DailyEntry.quantity), 0).label('total_milk')
    ).join(models.Customer, models.Customer.customer_id == models.DailyEntry.customer_id)
    query = query.filter(
        extract('year', models.DailyEntry.date) == year,
        extract('month', models.DailyEntry.date) == month
    ).group_by(models.DailyEntry.customer_id, models.Customer.name)
    query = query.order_by(desc('total_milk')).limit(count)
    return query.all()


def get_customer_portal(db: Session, customer_id: str, from_date=None, to_date=None):
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    entry_query = db.query(models.DailyEntry).filter(models.DailyEntry.customer_id == customer_id)
    if from_date:
        entry_query = entry_query.filter(models.DailyEntry.date >= from_date)
    if to_date:
        entry_query = entry_query.filter(models.DailyEntry.date <= to_date)
    entries = entry_query.order_by(models.DailyEntry.date.desc(), models.DailyEntry.session.desc()).all()
    payments = db.query(models.PaymentRecord).filter(models.PaymentRecord.customer_id == customer_id).order_by(models.PaymentRecord.from_date.desc()).all()
    total_milk = sum((e.quantity for e in entries), Decimal("0"))
    total_amount = sum((e.amount for e in entries), Decimal("0"))
    total_paid = sum((p.recorded_amount for p in payments if p.status == "Paid"), Decimal("0"))
    total_part_paid = sum((p.recorded_amount for p in payments if p.status == "Part Paid"), Decimal("0"))
    balance_due = total_amount - total_paid - total_part_paid + customer.opening_balance
    date_range = {}
    if entries:
        date_range = {"from": min(e.date for e in entries), "to": max(e.date for e in entries)}
    return {
        "customer": customer,
        "total_entries": len(entries),
        "total_milk": total_milk,
        "total_amount": total_amount,
        "balance_due": balance_due,
        "entries": entries,
        "payments": payments,
        "date_range": date_range
    }