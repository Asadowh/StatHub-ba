# Achievement Metrics Guide

## Available Metrics

When creating achievements, you must use one of these **metric** values:

### 1. `"matches"` - Number of Matches Played
- **Tracks**: Total number of matches a player has participated in
- **Example achievements**:
  - "First Match" - `target_value: 1`
  - "Reliable Starter" - `target_value: 5`
  - "Century Club" - `target_value: 100`

### 2. `"assists"` - Total Assists
- **Tracks**: Sum of all assists across all matches
- **Example achievements**:
  - "Helping Hand" - `target_value: 1`
  - "Playmaker" - `target_value: 10`
  - "Assist King" - `target_value: 50`

### 3. `"goals"` - Total Goals
- **Tracks**: Sum of all goals across all matches
- **Example achievements**:
  - "Maiden Goal" - `target_value: 1`
  - "Five-Goal Club" - `target_value: 5`
  - "Goal Machine" - `target_value: 30`
  - "Century Scorer" - `target_value: 100`

### 4. `"goals_per_match"` - Goals in a Single Match
- **Tracks**: Maximum goals scored in any single match
- **Example achievements**:
  - "Hat-trick Hero" - `target_value: 3` (score 3+ goals in one match)
  - "Quadruple" - `target_value: 4`
  - "Perfect Game" - `target_value: 5`

### 5. `"rating"` - Average Rating
- **Tracks**: Average rating across matches
- **Important**: Since `target_value` is stored as Integer in the database, store rating targets as `integer * 10`
  - For 7.5 rating → store `target_value: 75`
  - For 6.0 rating → store `target_value: 60`
  - For 10.0 rating → store `target_value: 100`
- **Special handling**: 
  - For "Elite Performer": Requires 5+ matches AND rating >= target
  - For other rating achievements: Uses average rating of available matches
- **Example achievements**:
  - "Elite Performer" - `target_value: 75` (7.5 rating, requires 5+ matches)
  - "Consistent Player" - `target_value: 60` (6.0 rating)
  - "Perfect 10" - `target_value: 100` (10.0 rating)

## Creating Custom Achievements

### Example 1: "10 Assists Club"
```json
{
  "name": "10 Assists Club",
  "description": "Provide 10 total assists",
  "tier": "Beginner",
  "metric": "assists",
  "target_value": 10,
  "points": 150
}
```

### Example 2: "Perfect Match"
```json
{
  "name": "Perfect Match",
  "description": "Score 5 goals in a single match",
  "tier": "Expert",
  "metric": "goals_per_match",
  "target_value": 5,
  "points": 500
}
```

### Example 3: "50 Matches Veteran"
```json
{
  "name": "50 Matches Veteran",
  "description": "Play 50 matches",
  "tier": "Advanced",
  "metric": "matches",
  "target_value": 50,
  "points": 400
}
```

## Important Notes

1. **Metric is case-sensitive**: Use exactly `"matches"`, `"assists"`, `"goals"`, `"goals_per_match"`, or `"rating"`

2. **Target value type**:
   - For `matches`, `assists`, `goals`, `goals_per_match`: Use integer (e.g., `5`)
   - For `rating`: Use float (e.g., `7.5`)

3. **Rating achievements**: 
   - If you create a custom rating achievement, it will use the average rating of all available matches
   - Only "Elite Performer" has special logic requiring 5+ matches

4. **Progress tracking**: All achievements are automatically tracked based on their metric, regardless of name!

## Tier Values

Use one of these tier values:
- `"Beginner"`
- `"Advanced"` (not "Hard")
- `"Expert"`

