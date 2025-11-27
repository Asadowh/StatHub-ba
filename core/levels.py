"""
Level System Configuration
Levels 1-10 with names, colors, and XP ranges
Progression is designed to be challenging - each level requires significantly more XP
"""

LEVEL_CONFIG = {
    1: {
        "name": "Rookie",
        "color": "#9CA3AF",  # Gray
        "min_xp": 0,
        "max_xp": 199,  # 200 XP needed (0-199)
    },
    2: {
        "name": "Amateur",
        "color": "#10B981",  # Green
        "min_xp": 200,
        "max_xp": 599,  # 400 XP needed (200-599)
    },
    3: {
        "name": "Rising Star",
        "color": "#3B82F6",  # Blue
        "min_xp": 600,
        "max_xp": 1499,  # 900 XP needed (600-1499)
    },
    4: {
        "name": "Professional",
        "color": "#8B5CF6",  # Purple
        "min_xp": 1500,
        "max_xp": 3499,  # 2000 XP needed (1500-3499)
    },
    5: {
        "name": "Elite",
        "color": "#F59E0B",  # Amber/Orange
        "min_xp": 3500,
        "max_xp": 7499,  # 4000 XP needed (3500-7499)
    },
    6: {
        "name": "Master",
        "color": "#EF4444",  # Red
        "min_xp": 7500,
        "max_xp": 14999,  # 7500 XP needed (7500-14999)
    },
    7: {
        "name": "Legend",
        "color": "#EC4899",  # Pink
        "min_xp": 15000,
        "max_xp": 29999,  # 15000 XP needed (15000-29999)
    },
    8: {
        "name": "Champion",
        "color": "#14B8A6",  # Teal
        "min_xp": 30000,
        "max_xp": 59999,  # 30000 XP needed (30000-59999)
    },
    9: {
        "name": "Icon",
        "color": "#F97316",  # Orange
        "min_xp": 60000,
        "max_xp": 124999,  # 65000 XP needed (60000-124999)
    },
    10: {
        "name": "Immortal",
        "color": "#EAB308",  # Gold/Yellow
        "min_xp": 125000,
        "max_xp": 999999,  # No upper limit, but requires 125000+ to reach
    },
}


def get_level_from_xp(xp: int) -> int:
    """Calculate level from XP"""
    for level in range(10, 0, -1):
        if xp >= LEVEL_CONFIG[level]["min_xp"]:
            return level
    return 1


def get_level_info(level: int) -> dict:
    """Get level information (name, color, XP range)"""
    return LEVEL_CONFIG.get(level, LEVEL_CONFIG[1])


def get_xp_progress(xp: int, level: int) -> dict:
    """Get XP progress within current level"""
    level_info = get_level_info(level)
    current_level_xp = xp - level_info["min_xp"]
    level_xp_range = level_info["max_xp"] - level_info["min_xp"] + 1
    progress_percent = (current_level_xp / level_xp_range) * 100 if level_xp_range > 0 else 100
    
    return {
        "current_xp": xp,
        "level": level,
        "level_name": level_info["name"],
        "level_color": level_info["color"],
        "xp_in_level": current_level_xp,
        "xp_for_next_level": level_info["max_xp"] - xp + 1 if level < 10 else None,
        "progress_percent": min(progress_percent, 100),
    }
