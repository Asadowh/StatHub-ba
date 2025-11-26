from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user
from schemas.user_schema import UserUpdate
from services.user_service import update_user

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.put("/", response_model=dict)
def update_settings(data: UserUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    update_user(db, user, data)
    return {"message": "Settings updated"}
