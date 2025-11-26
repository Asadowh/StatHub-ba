from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user
from schemas.user_schema import UserResponse, UserUpdate
from services.user_service import update_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_me(data: UserUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_user(db, current_user, data)
