from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(db: Session, user: User, data):
    # Use model_dump for Pydantic V2, fallback to dict for V1
    if hasattr(data, 'model_dump'):
        update_data = data.model_dump(exclude_unset=True)
    else:
        update_data = data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user
