"""
Skill Tree System for Autogenesis AI.
Tracks skills learned at each level.
"""
import json
from pathlib import Path

SKILLS_FILE = Path("storage/skills.json")

# Skill tree definition
SKILL_TREE = {
    "Baby": {
        "level_min": 0,
        "skills": [
            {"id": "html", "name": "HTML Basics", "icon": "📄"},
            {"id": "css", "name": "CSS Styling", "icon": "🎨"},
        ]
    },
    "Child": {
        "level_min": 10,
        "skills": [
            {"id": "js", "name": "JavaScript", "icon": "⚡"},
            {"id": "python", "name": "Python Basics", "icon": "🐍"},
            {"id": "json", "name": "JSON/APIs", "icon": "📦"},
        ]
    },
    "Teen": {
        "level_min": 25,
        "skills": [
            {"id": "api", "name": "REST APIs", "icon": "🌐"},
            {"id": "docker", "name": "Docker", "icon": "🐳"},
            {"id": "testing", "name": "Unit Testing", "icon": "🧪"},
        ]
    },
    "Adult": {
        "level_min": 50,
        "skills": [
            {"id": "react", "name": "React/Next.js", "icon": "⚛️"},
            {"id": "flask", "name": "Flask/FastAPI", "icon": "🔥"},
            {"id": "cicd", "name": "CI/CD Pipelines", "icon": "🔄"},
            {"id": "sql", "name": "Databases", "icon": "🗄️"},
        ]
    },
    "Expert": {
        "level_min": 75,
        "skills": [
            {"id": "auth", "name": "Authentication", "icon": "🔐"},
            {"id": "deploy", "name": "Cloud Deploy", "icon": "☁️"},
            {"id": "perf", "name": "Performance", "icon": "⚡"},
            {"id": "security", "name": "Security", "icon": "🛡️"},
        ]
    },
    "Sage": {
        "level_min": 95,
        "skills": [
            {"id": "arch", "name": "System Design", "icon": "🏗️"},
            {"id": "ml", "name": "ML Integration", "icon": "🤖"},
            {"id": "scale", "name": "Scalability", "icon": "📈"},
            {"id": "mentor", "name": "Code Review", "icon": "👁️"},
        ]
    }
}

def get_unlocked_skills(level: int) -> dict:
    """Get all skills unlocked at current level."""
    unlocked = []
    locked = []
    current_stage = "Baby"
    
    for stage_name, stage_data in SKILL_TREE.items():
        if level >= stage_data["level_min"]:
            current_stage = stage_name
            for skill in stage_data["skills"]:
                unlocked.append({**skill, "stage": stage_name, "unlocked": True})
        else:
            for skill in stage_data["skills"]:
                locked.append({**skill, "stage": stage_name, "unlocked": False})
    
    return {
        "current_stage": current_stage,
        "unlocked": unlocked,
        "locked": locked,
        "total_unlocked": len(unlocked),
        "total_skills": len(unlocked) + len(locked)
    }

def get_skill_tree_data(level: int) -> dict:
    """Get complete skill tree data for UI."""
    skills = get_unlocked_skills(level)
    
    stages = []
    for stage_name, stage_data in SKILL_TREE.items():
        is_unlocked = level >= stage_data["level_min"]
        is_current = skills["current_stage"] == stage_name
        
        stages.append({
            "name": stage_name,
            "level_min": stage_data["level_min"],
            "unlocked": is_unlocked,
            "current": is_current,
            "skills": [
                {**s, "unlocked": is_unlocked} 
                for s in stage_data["skills"]
            ]
        })
    
    return {
        "stages": stages,
        "current_stage": skills["current_stage"],
        "unlocked_count": skills["total_unlocked"],
        "total_count": skills["total_skills"],
        "progress_percent": round(skills["total_unlocked"] / skills["total_skills"] * 100)
    }

def award_skill_badge(skill_id: str) -> bool:
    """Award a specific skill badge (for manual unlocks)."""
    SKILLS_FILE.parent.mkdir(exist_ok=True)
    
    badges = []
    if SKILLS_FILE.exists():
        badges = json.loads(SKILLS_FILE.read_text())
    
    if skill_id not in badges:
        badges.append(skill_id)
        SKILLS_FILE.write_text(json.dumps(badges))
        return True
    return False

def get_badges() -> list:
    """Get all earned badges."""
    if SKILLS_FILE.exists():
        return json.loads(SKILLS_FILE.read_text())
    return []
