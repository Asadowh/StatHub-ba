from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.search_service import search_players, search_matches

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search(q: str = Query(...), db: Session = Depends(get_db)):
    return {
        "players": search_players(db, q),
        "matches": search_matches(db, q)
    }
