# How to Seed Achievements

## Quick Method (Recommended)

### Step 1: Start your FastAPI server
```bash
cd C:\Users\vaqif\OneDrive\Desktop\StatHub-backend
.\venv\Scripts\activate
uvicorn main:app --reload
```

### Step 2: Seed via Swagger UI
1. Open http://localhost:8000/docs in your browser
2. Find `POST /achievements/seed`
3. Click "Authorize" (top right) and enter your admin JWT token
4. Click "Try it out" → "Execute"
5. This will:
   - ✅ Create all 9 achievements
   - ✅ Check all existing players and unlock achievements they've already earned
   - ✅ Update progress for all players

### Step 3: Verify
- Check `GET /achievements/` - should return 9 achievements
- Check a player's achievements: `GET /achievements/user/{user_id}`
- Progress should show `current_value / target_value`

## Alternative: Via Python Script

### Option A: Direct Script (if imports work)
```bash
cd C:\Users\vaqif\OneDrive\Desktop\StatHub-backend
.\venv\Scripts\python scripts\seed_achievements.py
```

### Option B: Via API Script
```bash
cd C:\Users\vaqif\OneDrive\Desktop\StatHub-backend
.\venv\Scripts\python scripts\seed_via_api.py
```
(You'll need to provide your admin JWT token)

## Progress Tracking

Progress is automatically tracked:
- ✅ When a stat is created → achievements are checked
- ✅ `current_value` is updated for all achievements
- ✅ Achievements unlock automatically when conditions are met
- ✅ Frontend shows progress bar: `current_value / target_value`

## Manual Refresh

If you need to manually refresh achievements for a user:
- `POST /achievements/me/refresh` - Refresh current user's achievements
- `POST /achievements/check-all` - Check all players (admin only)

## Achievement List

1. **First Match** - Play 1 match
2. **Helping Hand** - Get 1 assist
3. **Maiden Goal** - Score 1 goal
4. **Five-Goal Club** - Score 5 goals
5. **Reliable Starter** - Play 5 matches
6. **Hat-trick Hero** - Score 3 goals in one match
7. **Goal Machine** - Score 30 goals
8. **Elite Performer** - Average rating 7.5+ across 5 matches
9. **Century Scorer** - Score 100 goals


