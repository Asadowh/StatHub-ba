from fastapi import FastAPI
from database import engine, Base
from routers import auth, matches, stats, trophies, search, news, comments, reactions, ratings
import models.user
import models.match
import models.stat
import models.trophy
import models.news
import models.rating
import models.comment
import models.reaction

# Initialize FastAPI app
app = FastAPI(
    title="StatHub Backend",
    version="1.0.7",
    description="Backend API for StatHub – football player stats, matches, trophies, search, news, comments, reactions, and authentication."
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(stats.router)
app.include_router(trophies.router)
app.include_router(search.router)
app.include_router(news.router)
app.include_router(comments.router)
app.include_router(reactions.router)
app.include_router(ratings.router)

# Root route
@app.get("/")
def root():
    return {"AMCUGUVU YEYIM SEMAYE, HEMEN NOMREDEYEM ZENG ELE MAA"}
