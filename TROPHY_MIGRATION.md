# Trophy System Database Migration

## Changes Made

The Trophy model has been updated to support automatic trophy awarding based on match performance:

**Old Structure:**
- `name` (String)
- `description` (String, nullable)
- `awarded_to` (Integer, ForeignKey to users)

**New Structure:**
- `match_id` (Integer, ForeignKey to matches, UNIQUE)
- `awarded_to` (Integer, ForeignKey to users)
- `date_awarded` (DateTime)

## Migration Steps

### Option 1: Fresh Start (Recommended if you don't have important trophy data)

```sql
-- Drop existing trophies table
DROP TABLE IF EXISTS trophies CASCADE;

-- Create new trophies table
CREATE TABLE trophies (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL UNIQUE REFERENCES matches(id) ON DELETE CASCADE,
    awarded_to INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date_awarded TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_trophies_awarded_to ON trophies(awarded_to);
CREATE INDEX idx_trophies_match_id ON trophies(match_id);
```

### Option 2: Migrate Existing Data (If you have trophies you want to keep)

**Note:** This migration assumes you can map existing trophies to matches. If you can't, you'll need to drop the old trophies.

```sql
-- Step 1: Add new columns
ALTER TABLE trophies ADD COLUMN IF NOT EXISTS match_id INTEGER;
ALTER TABLE trophies ADD COLUMN IF NOT EXISTS date_awarded TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;

-- Step 2: If you have a way to map old trophies to matches, update match_id
-- Otherwise, you'll need to delete old trophies:
-- DELETE FROM trophies WHERE match_id IS NULL;

-- Step 3: Make match_id NOT NULL and add unique constraint
ALTER TABLE trophies ALTER COLUMN match_id SET NOT NULL;
ALTER TABLE trophies ADD CONSTRAINT uq_trophy_match_id UNIQUE (match_id);

-- Step 4: Remove old columns
ALTER TABLE trophies DROP COLUMN IF EXISTS name;
ALTER TABLE trophies DROP COLUMN IF EXISTS description;

-- Step 5: Create indexes
CREATE INDEX IF NOT EXISTS idx_trophies_awarded_to ON trophies(awarded_to);
CREATE INDEX IF NOT EXISTS idx_trophies_match_id ON trophies(match_id);
```

## After Migration

1. **Test the trophy system:**
   - Create a match with player stats
   - Verify that a trophy is automatically awarded to the player with the highest rating
   - Check tiebreaker logic (goals → assists → earliest stat)

2. **Recalculate existing trophies (if needed):**
   If you have existing matches with stats but no trophies, you can run this Python script:

```python
from database import SessionLocal
from services.trophy_service import award_trophy_for_match
from models.match import Match

db = SessionLocal()
try:
    # Get all matches
    matches = db.query(Match).all()
    
    for match in matches:
        # Award trophy if not already awarded
        award_trophy_for_match(db, match.id)
        print(f"Processed match {match.id}")
    
    db.commit()
    print("All matches processed!")
finally:
    db.close()
```

## Verification

After migration, verify:
- ✅ Trophy table has `match_id` column with UNIQUE constraint
- ✅ Trophy table has `awarded_to` column
- ✅ Trophy table has `date_awarded` column
- ✅ Old `name` and `description` columns are removed
- ✅ Indexes are created
- ✅ Creating a match with stats automatically awards a trophy


