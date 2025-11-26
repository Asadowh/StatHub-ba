from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.security import get_current_user

from schemas.reaction_schema import ReactionCreate, ReactionResponse
from services.reaction_service import create_reaction

router = APIRouter(prefix="/reactions", tags=["Reactions"])

@router.post("/", response_model=ReactionResponse)
def react(data: ReactionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_reaction(db, data, user.id)
