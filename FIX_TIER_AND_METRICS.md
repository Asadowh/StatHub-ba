# Fix Tier and Metrics Issues

## Issue 1: Tier "Hard" → "Advanced"

If you have existing achievements in the database with `tier = "Hard"`, update them:

### SQL Query (Run in your database):
```sql
UPDATE achievements SET tier = 'Advanced' WHERE tier = 'Hard';
```

Or update via API:
1. Get all achievements: `GET /achievements/`
2. Find ones with `tier: "Hard"`
3. Update them individually (if you have an update endpoint)

## Issue 2: Custom Achievements Not Tracking

**FIXED!** The achievement checker now uses `metric` instead of `name`, so custom achievements will be tracked automatically.

### Available Metrics:

1. **`"matches"`** - Total matches played
2. **`"assists"`** - Total assists
3. **`"goals"`** - Total goals
4. **`"goals_per_match"`** - Goals in a single match (max)
5. **`"rating"`** - Average rating

### How It Works Now:

- ✅ Achievements are tracked by **metric**, not by name
- ✅ Custom achievements with valid metrics will be tracked automatically
- ✅ No need to hardcode achievement names anymore

### Example Custom Achievement:

```json
POST /achievements/
{
  "name": "My Custom Achievement",
  "description": "Score 20 goals",
  "tier": "Advanced",
  "metric": "goals",
  "target_value": 20,
  "points": 250
}
```

This will automatically track progress based on the `"goals"` metric!

## Testing

1. **Fix tier**: Run the SQL query above
2. **Test custom achievement**: Create one with a valid metric
3. **Check progress**: Create stats and see if achievement tracks correctly


