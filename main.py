from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base

# Import models for table creation
import models.user
import models.match
import models.stat
import models.rating
import models.trophy
import models.news
import models.comment
import models.reaction
import models.achievement

# Routers
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

app = FastAPI(
    title="StatHub Backend",
    version="1.0.0",
    description="Backend API for StatHub."
)

# Static files (if folder exists)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    print("⚠️ Static folder not found. Skipping mount.")

# Uploads (if used)
try:
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
except:
    print("⚠️ Uploads folder not found. Skipping mount.")

# CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://stathub-delta.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("📦 Tables ready.")

    # Auto-seed achievements (safe mode)
    try:
        from scripts.seed_achievements import seed_achievements
        from database import SessionLocal

        db = SessionLocal()
        seed_achievements(db, check_existing_players=True)
        db.close()
        print("🌱 Achievements seeded.")
    except Exception as e:
        print("⚠️ Achievement seeding skipped:", e)

# Routers
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

@app.get("/")
def root():
    return {"message": "StatHub API is running 🚀"}
