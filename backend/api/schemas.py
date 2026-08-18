from pydantic import BaseModel, Field, ConfigDict, EmailStr
from decimal import Decimal
from datetime import date, datetime
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool

class CustomerBase(BaseModel):
    customer_id: str = Field(..., max_length=20)
    name: str = Field(..., max_length=100)
    milk_no: Optional[str] = Field(None, max_length=20)
    phone: Optional[str] = Field(None, max_length=20)
    village: Optional[str] = Field(None, max_length=100)
    opening_balance: Decimal = Decimal("0")
    status: str = Field(default="Active", max_length=20)
    start_date: Optional[date] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class DailyEntryBase(BaseModel):
    date: date
    session: str = Field(..., pattern="^(AM|PM)$")
    customer_id: str
    quantity: Decimal = Field(..., ge=0)
    rate: Decimal = Field(..., ge=0)
    amount: Decimal = Field(..., ge=0)

class DailyEntryCreate(DailyEntryBase):
    pass

class DailyEntryResponse(DailyEntryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer: Optional[CustomerResponse] = None

class PaymentRecordBase(BaseModel):
    customer_id: str
    from_date: date
    end_date: date
    recorded_amount: Decimal = Field(..., ge=0)
    status: Optional[str] = Field(default="Pending", max_length=50)
    notes: Optional[str] = None

class PaymentRecordCreate(PaymentRecordBase):
    pass

class PaymentRecordResponse(PaymentRecordBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: Optional[datetime] = None
    customer: Optional[CustomerResponse] = None

class DashboardSummary(BaseModel):
    active_customers: int
    today_milk: Decimal
    today_amount: Decimal
    month_milk: Decimal
    month_amount: Decimal
    total_milk: Decimal
    total_amount: Decimal
    today_date: date

class DateWiseSummary(BaseModel):
    date: date
    total_milk: Decimal
    total_amount: Decimal
    am_count: int
    pm_count: int
    am_milk: Decimal
    pm_milk: Decimal

class CustomerMonthlyMilkSummary(BaseModel):
    month: int
    total_milk: Decimal

class TopCustomerMonthSummary(BaseModel):
    customer_id: str
    customer_name: str
    total_milk: Decimal

class CustomerPortalResponse(BaseModel):
    customer: CustomerResponse
    total_entries: int
    total_milk: Decimal
    total_amount: Decimal
    balance_due: Decimal
    entries: List[DailyEntryResponse]
    payments: List[PaymentRecordResponse]
    date_range: dict

class SettingBase(BaseModel):
    key: str
    value: Optional[str] = None

class SettingResponse(SettingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int