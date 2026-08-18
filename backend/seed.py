from api.database import SessionLocal, engine
from api import models
from api.auth import get_password_hash
from datetime import date
from decimal import Decimal

def seed():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.User).first():
            print("Already seeded")
            return
        
        admin = models.User(email="admin@milk.local", full_name="Admin", hashed_password=get_password_hash("admin123"))
        db.add(admin)

        customers = [
            models.Customer(customer_id="C003", name="Koothayi", milk_no="M001", phone="9000000001", village="Sillakudi", opening_balance=Decimal("0"), status="Active", start_date=date(2026,7,16)),
            models.Customer(customer_id="C004", name="Maruthamuthu", milk_no="M002", phone="9000000002", village="Sillakudi", opening_balance=Decimal("0"), status="Active", start_date=date(2026,7,16)),
            models.Customer(customer_id="C010", name="Iswarya", milk_no="M003", phone="9000000003", village="Sillakudi", opening_balance=Decimal("0"), status="Active", start_date=date(2026,7,16)),
            models.Customer(customer_id="C012", name="Gunasekaran", milk_no="M004", phone="9000000004", village="Sillakudi", opening_balance=Decimal("0"), status="Active", start_date=date(2026,7,16)),
            models.Customer(customer_id="C013", name="Chinnayan", milk_no="M005", phone="9000000005", village="Sillakudi", opening_balance=Decimal("0"), status="Active", start_date=date(2026,7,16)),
        ]
        db.add_all(customers)
        db.commit()

        entries = [
            models.DailyEntry(date=date(2026,7,16), session="AM", customer_id="C003", quantity=Decimal("6.8"),  rate=Decimal("35"), amount=Decimal("238")),
            models.DailyEntry(date=date(2026,7,16), session="PM", customer_id="C003", quantity=Decimal("7.0"),  rate=Decimal("35"), amount=Decimal("245")),
            models.DailyEntry(date=date(2026,7,17), session="AM", customer_id="C003", quantity=Decimal("6.8"),  rate=Decimal("35"), amount=Decimal("238")),
            models.DailyEntry(date=date(2026,7,17), session="PM", customer_id="C003", quantity=Decimal("7.0"),  rate=Decimal("35"), amount=Decimal("245")),
            models.DailyEntry(date=date(2026,7,18), session="AM", customer_id="C003", quantity=Decimal("5.6"),  rate=Decimal("35"), amount=Decimal("196")),
            models.DailyEntry(date=date(2026,7,18), session="PM", customer_id="C003", quantity=Decimal("7.5"),  rate=Decimal("35"), amount=Decimal("262.5")),
            models.DailyEntry(date=date(2026,7,16), session="AM", customer_id="C004", quantity=Decimal("5.8"),  rate=Decimal("35"), amount=Decimal("203")),
            models.DailyEntry(date=date(2026,7,16), session="PM", customer_id="C004", quantity=Decimal("6.2"),  rate=Decimal("35"), amount=Decimal("217")),
            models.DailyEntry(date=date(2026,7,17), session="AM", customer_id="C004", quantity=Decimal("5.7"),  rate=Decimal("35"), amount=Decimal("199.5")),
            models.DailyEntry(date=date(2026,7,17), session="PM", customer_id="C004", quantity=Decimal("5.9"),  rate=Decimal("35"), amount=Decimal("206.5")),
            models.DailyEntry(date=date(2026,7,18), session="AM", customer_id="C004", quantity=Decimal("6.6"),  rate=Decimal("35"), amount=Decimal("231")),
            models.DailyEntry(date=date(2026,7,18), session="PM", customer_id="C004", quantity=Decimal("5.4"),  rate=Decimal("35"), amount=Decimal("189")),
            models.DailyEntry(date=date(2026,7,16), session="AM", customer_id="C010", quantity=Decimal("2.7"),  rate=Decimal("35"), amount=Decimal("94.5")),
            models.DailyEntry(date=date(2026,7,16), session="PM", customer_id="C010", quantity=Decimal("3.4"),  rate=Decimal("35"), amount=Decimal("119")),
            models.DailyEntry(date=date(2026,7,17), session="AM", customer_id="C010", quantity=Decimal("2.1"),  rate=Decimal("35"), amount=Decimal("73.5")),
            models.DailyEntry(date=date(2026,7,16), session="AM", customer_id="C012", quantity=Decimal("2.8"),  rate=Decimal("35"), amount=Decimal("98")),
            models.DailyEntry(date=date(2026,7,17), session="AM", customer_id="C012", quantity=Decimal("2.3"),  rate=Decimal("35"), amount=Decimal("80.5")),
            models.DailyEntry(date=date(2026,7,18), session="AM", customer_id="C012", quantity=Decimal("3.1"),  rate=Decimal("35"), amount=Decimal("108.5")),
            models.DailyEntry(date=date(2026,7,16), session="AM", customer_id="C013", quantity=Decimal("8.9"),  rate=Decimal("35"), amount=Decimal("311.5")),
            models.DailyEntry(date=date(2026,7,16), session="PM", customer_id="C013", quantity=Decimal("8.6"),  rate=Decimal("35"), amount=Decimal("301")),
            models.DailyEntry(date=date(2026,7,17), session="AM", customer_id="C013", quantity=Decimal("8.9"),  rate=Decimal("35"), amount=Decimal("311.5")),
            models.DailyEntry(date=date(2026,7,17), session="PM", customer_id="C013", quantity=Decimal("9.3"),  rate=Decimal("35"), amount=Decimal("325.5")),
            models.DailyEntry(date=date(2026,7,18), session="AM", customer_id="C013", quantity=Decimal("8.7"),  rate=Decimal("35"), amount=Decimal("304.5")),
            models.DailyEntry(date=date(2026,7,18), session="PM", customer_id="C013", quantity=Decimal("8.9"),  rate=Decimal("35"), amount=Decimal("311.5")),
        ]
        db.add_all(entries)
        
        settings = [models.Setting(key="default_rate", value="35"), models.Setting(key="max_rows", value="50000")]
        db.add_all(settings)
        
        db.commit()
        print("Seeded 5 customers with AM/PM entries successfully")
    finally:
        db.close()

if __name__ == "__main__":
    seed()