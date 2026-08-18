from fastapi import APIRouter
from api.v1.endpoints import auth, customers, daily_entries, payments, dashboard, portal, settings, google_sheets

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(daily_entries.router, prefix="/daily-entries", tags=["daily-entries"])
api_router.include_router(payments.router, prefix="/payment-records", tags=["payments"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(portal.router, prefix="/customer-portal", tags=["portal"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
# include google sheets export endpoints under /export
api_router.include_router(google_sheets.router, prefix="/export", tags=["export"])