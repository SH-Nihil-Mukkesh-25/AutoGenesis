"""
Intelligence System - Tracks Autogenesis growth and learning.
"""
import json
from pathlib import Path

STATS_FILE = Path("storage/intelligence.json")

# Growth stages
STAGES = [
    {"min": 0,  "name": "Baby", "emoji": "👶", "desc": "Just born, learning basics"},
    {"min": 10, "name": "Child", "emoji": "🧒", "desc": "Starting to understand"},
    {"min": 25, "name": "Teen", "emoji": "🧑", "desc": "Getting competent"},
    {"min": 50, "name": "Adult", "emoji": "🧑‍💼", "desc": "Skilled developer"},
    {"min": 75, "name": "Expert", "emoji": "🧙", "desc": "Master of code"},
    {"min": 95, "name": "Sage", "emoji": "🏆", "desc": "Legendary AI"},
]

def get_stats() -> dict:
    """Load or initialize stats."""
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text())
        except:
            pass
    
    return {
        "total_projects": 0,
        "total_files": 0,
        "total_issues_found": 0,
        "total_issues_fixed": 0,
        "languages_used": [],
        "xp": 0,
        "level": 0
    }

def save_stats(stats: dict):
    """Save stats to file."""
    STATS_FILE.parent.mkdir(exist_ok=True)
    STATS_FILE.write_text(json.dumps(stats, indent=2))

def calculate_level(xp: int) -> int:
    """Calculate level percentage (0-100) from XP."""
    # XP curve: level = sqrt(xp) * 10, capped at 100
    import math
    level = min(100, int(math.sqrt(xp) * 10))
    return level

def get_stage(level: int) -> dict:
    """Get the current growth stage based on level."""
    current_stage = STAGES[0]
    for stage in STAGES:
        if level >= stage["min"]:
            current_stage = stage
    return current_stage

def add_project_xp(files_generated: int, issues_found: int, languages: list) -> dict:
    """
    Add XP for completing a project.
    Returns updated stats.
    """
    stats = get_stats()
    
    # Base XP for completing a project
    xp_gained = 10
    
    # Bonus for multiple files
    xp_gained += files_generated * 2
    
    # Bonus for clean code (fewer issues)
    if issues_found == 0:
        xp_gained += 15  # Perfect code bonus
    elif issues_found <= 2:
        xp_gained += 5   # Minor issues bonus
    
    # Bonus for using new languages
    for lang in languages:
        if lang not in stats["languages_used"]:
            xp_gained += 10  # New language bonus
            stats["languages_used"].append(lang)
    
    # Update stats
    stats["total_projects"] += 1
    stats["total_files"] += files_generated
    stats["total_issues_found"] += issues_found
    stats["xp"] += xp_gained
    stats["level"] = calculate_level(stats["xp"])
    
    save_stats(stats)
    
    return {
        "xp_gained": xp_gained,
        "total_xp": stats["xp"],
        "level": stats["level"],
        "stage": get_stage(stats["level"]),
        "stats": stats
    }

def get_intelligence() -> dict:
    """Get current intelligence status."""
    stats = get_stats()
    level = calculate_level(stats["xp"])
    stage = get_stage(level)
    
    return {
        "level": level,
        "xp": stats["xp"],
        "stage_name": stage["name"],
        "stage_emoji": stage["emoji"],
        "stage_desc": stage["desc"],
        "total_projects": stats["total_projects"],
        "total_files": stats["total_files"],
        "languages": stats["languages_used"],
        "next_stage": get_next_stage(level)
    }

def get_next_stage(level: int) -> dict:
    """Get the next stage to reach."""
    for stage in STAGES:
        if stage["min"] > level:
            return {
                "name": stage["name"],
                "emoji": stage["emoji"],
                "xp_needed": stage["min"] - level
            }
    return None
