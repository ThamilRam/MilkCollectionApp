from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import models, schemas
from api.database import get_db
from api.auth import get_current_user

router = APIRouter()

@router.get("/")
def get_settings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    settings = db.query(models.Setting).all()
    return {s.key: s.value for s in settings}

@router.get("/{key}")
def get_setting(key: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    setting = db.query(models.Setting).filter(models.Setting.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": setting.key, "value": setting.value}

@router.put("/{key}")
def update_setting(key: str, value: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    setting = db.query(models.Setting).filter(models.Setting.key == key).first()
    if not setting:
        setting = models.Setting(key=key, value=value)
        db.add(setting)
    else:
        setting.value = value
    db.commit()
    db.refresh(setting)
    return {"key": setting.key, "value": setting.value}