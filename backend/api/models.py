from sqlalchemy import Integer, String, Numeric, Date, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from decimal import Decimal
from typing import Optional
from api.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    full_name: Mapped[str] = mapped_column(String(100))

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    milk_no: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    village: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    opening_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    status: Mapped[str] = mapped_column(String(20), default="Active")
    start_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    isMilkcustomer: Mapped[bool] = mapped_column("is_milk_customer", Boolean, default=True, nullable=False)

    entries: Mapped[list["DailyEntry"]] = relationship(back_populates="customer", cascade="all, delete-orphan")
    payments: Mapped[list["PaymentRecord"]] = relationship(back_populates="customer", cascade="all, delete-orphan")
    purchases: Mapped[list["PurchaseRecord"]] = relationship(back_populates="customer", cascade="all, delete-orphan")

class DailyEntry(Base):
    __tablename__ = "daily_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[Date] = mapped_column(Date, index=True)
    session: Mapped[str] = mapped_column(String(10))
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    rate: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    customer: Mapped["Customer"] = relationship(back_populates="entries")

class PaymentRecord(Base):
    __tablename__ = "payment_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"))
    from_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
    recorded_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(50), default="Pending")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped["Customer"] = relationship(back_populates="payments")

class Setting(Base):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(100), unique=True)
    value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_name: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    active: Mapped[bool] = mapped_column(default=True)
    purchases: Mapped[list["PurchaseRecord"]] = relationship(back_populates="product")

class PurchaseRecord(Base):
    __tablename__ = "purchase_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped["Customer"] = relationship(back_populates="purchases")
    product: Mapped["Product"] = relationship(back_populates="purchases")