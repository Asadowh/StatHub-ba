# Achievement System - Complete Explanation

## ✅ Fixed Issues

### 1. Tier "Hard" → "Advanced"
**Problem**: Frontend was looking for "Hard" but backend uses "Advanced"

**Solution**: 
- Frontend updated to use "Advanced"
- If you have existing achievements with "Hard" tier, run:
  ```sql
  UPDATE achievements SET tier = 'Advanced' WHERE tier = 'Hard';
  ```

### 2. Custom Achievements Not Tracking
**Problem**: Achievement checker only tracked achievements by exact name (hardcoded)

**Solution**: 
- ✅ **FIXED!** Achievement checker now uses `metric` field instead of name
- Custom achievements will now be tracked automatically if they use a valid metric

## Available Metrics

When creating achievements, use one of these **metric** values:

| Metric | What It Tracks | Example `target_value` |
|--------|---------------|----------------------|
| `"matches"` | Total matches played | `1`, `5`, `50`, `100` |
| `"assists"` | Total assists across all matches | `1`, `10`, `50` |
| `"goals"` | Total goals across all matches | `1`, `5`, `30`, `100` |
| `"goals_per_match"` | Maximum goals in any single match | `3` (hat-trick), `4`, `5` |
| `"rating"` | Average rating | `75` (for 7.5), `60` (for 6.0), `100` (for 10.0) |

### Important Notes:

1. **Rating achievements**: Store `target_value` as `integer * 10`
   - 7.5 rating → `target_value: 75`
   - 6.0 rating → `target_value: 60`
   - 10.0 rating → `target_value: 100`

2. **Tier values**: Use `"Beginner"`, `"Advanced"`, or `"Expert"`

## How Custom Achievements Work Now

### Before (Broken):
```python
if achievement.name == "First Match":  # Only works for exact name
    # track progress
```

### After (Fixed):
```python
if achievement.metric == "matches":  # Works for ANY achievement with this metric
    # track progress
```

## Examples

### Example 1: Custom "20 Goals" Achievement
```json
POST /achievements/
{
  "name": "Twenty Goal Hero",
  "description": "Score 20 total goals",
  "tier": "Advanced",
  "metric": "goals",
  "target_value": 20,
  "points": 300
}
```
✅ **Will be tracked automatically!** Progress updates when player scores goals.

### Example 2: Custom "10 Matches" Achievement
```json
POST /achievements/
{
  "name": "Ten Matches",
  "description": "Play 10 matches",
  "tier": "Beginner",
  "metric": "matches",
  "target_value": 10,
  "points": 150
}
```
✅ **Will be tracked automatically!** Progress updates when player plays matches.

### Example 3: Custom Rating Achievement
```json
POST /achievements/
{
  "name": "Excellent Player",
  "description": "Maintain 8.0+ average rating",
  "tier": "Advanced",
  "metric": "rating",
  "target_value": 80,  // 8.0 * 10
  "points": 300
}
```
✅ **Will be tracked automatically!** Progress updates based on average rating.

## Testing Custom Achievements

1. Create a custom achievement via `POST /achievements/`
2. Create stats for a player (goals, assists, matches, etc.)
3. Check achievements: `GET /achievements/user/{user_id}`
4. Progress should update automatically!

## Summary

- ✅ **Custom achievements now work** - tracked by metric, not name
- ✅ **5 metrics available**: matches, assists, goals, goals_per_match, rating
- ✅ **Tier fixed**: Use "Advanced" not "Hard"
- ✅ **Rating targets**: Store as integer*10 (75 for 7.5)



