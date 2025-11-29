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
    "http://localhost:8080",  # Frontend dev server
    "http://localhost:3000",  # Alternative frontend port
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
    "*",  # Fallback: allow all for now (you can lock later)
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
    
    # Seed achievements automatically on startup
    try:
        from scripts.seed_achievements import seed_achievements
        from database import SessionLocal
        db = SessionLocal()
        try:
            seed_achievements(db, check_existing_players=False)  # Don't check players on startup for performance
            print("🌱 Achievements seeded successfully.")
        finally:
            db.close()
    except Exception as e:
        # Don't crash the server if seeding fails - just log it
        print(f"⚠️  Warning: Could not seed achievements on startup: {e}")
        print("   You can manually seed achievements via POST /achievements/seed endpoint.")


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
