from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

# Import all models so they are registered for table creation
import models.user
import models.match
import models.stat
import models.rating
import models.trophy
import models.news
import models.comment
import models.reaction
import models.achievement

# Import routers
from routers import (
    auth,
    users,
    matches,
    stats,
    ratings,
    trophies,
    news,
    comments,
    reactions,
    achievements,
    search,
    dashboard,
    settings,
    leaderboard
)

# ---------------------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------------------
app = FastAPI(
    title="StatHub Backend",
    version="1.0.0",
    description="Backend API for StatHub – authentication, profiles, stats, matches, news, reactions, trophies, achievements, dashboard, and search."
)

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
# ---------------------------------------------------------
# CORS (FRONTEND ACCESS)
# ---------------------------------------------------------
origins = [
    "*",  # allow all for now (you can lock later)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Create Tables at Startup
# ---------------------------------------------------------
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print("📦 Database tables created / verified.")


# ---------------------------------------------------------
# Routers Registration
# ---------------------------------------------------------
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(matches.router)
app.include_router(stats.router)
app.include_router(ratings.router)
app.include_router(trophies.router)
app.include_router(news.router)
app.include_router(comments.router)
app.include_router(reactions.router)
app.include_router(achievements.router)
app.include_router(search.router)
app.include_router(dashboard.router)
app.include_router(settings.router)
app.include_router(leaderboard.router)


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "StatHub API is running 🚀"}
