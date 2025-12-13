"""
Planner Module - Smart project structure planning.
"""
from .agent import run_agent
import json

def generate_plan(idea: str):
    """
    Generates a smart project plan with appropriate files for the technology.
    """
    prompt = f"""You are an expert software architect. Plan a project for:

IDEA: {idea}

Analyze the idea and determine:
1. What technology/language is best suited
2. What files are needed for a complete, working project

Return ONLY valid JSON:
{{
    "project_name": "project-name",
    "description": "Brief description",
    "tech_stack": ["Python", "Flask"],
    "phases": [
        {{"name": "Phase 1: Setup", "tasks": ["task1", "task2"]}}
    ],
    "files": [
        {{"path": "main.py", "description": "Main entry point", "language": "Python"}},
        {{"path": "templates/index.html", "description": "Homepage", "language": "HTML"}}
    ]
}}

FILE GUIDELINES:
- For web apps: include HTML, CSS, JS files
- For APIs: include routes, models, config files
- For CLI tools: include main.py, utils.py
- Always include appropriate file extensions
- Match file language to extension (.py=Python, .html=HTML, .js=JavaScript)

Keep it focused: 2-5 files for simple ideas, 5-10 for complex ones.
Return ONLY the JSON."""
    
    result = run_agent(prompt, mode="plan")
    
    # Parse result
    if isinstance(result, dict):
        if "phases" in result and "files" in result:
            return result
        
        if "response" in result:
            try:
                text = result["response"]
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    parsed = json.loads(text[start:end])
                    if "files" not in parsed:
                        parsed["files"] = detect_files(idea)
                    return parsed
            except:
                pass
    
    # Smart fallback based on idea keywords
    return create_smart_fallback(idea)

def detect_files(idea: str) -> list:
    """Detect appropriate files based on idea keywords."""
    idea_lower = idea.lower()
    
    if any(w in idea_lower for w in ["web", "website", "html", "frontend"]):
        return [
            {"path": "index.html", "description": "Main HTML page", "language": "HTML"},
            {"path": "styles.css", "description": "Stylesheet", "language": "CSS"},
            {"path": "main.js", "description": "JavaScript logic", "language": "JavaScript"},
        ]
    elif any(w in idea_lower for w in ["api", "rest", "backend", "server"]):
        return [
            {"path": "app.py", "description": "Flask/FastAPI server", "language": "Python"},
            {"path": "routes.py", "description": "API routes", "language": "Python"},
            {"path": "models.py", "description": "Data models", "language": "Python"},
        ]
    elif any(w in idea_lower for w in ["react", "next", "component"]):
        return [
            {"path": "App.tsx", "description": "Main React component", "language": "TypeScript React"},
            {"path": "index.tsx", "description": "Entry point", "language": "TypeScript React"},
            {"path": "styles.css", "description": "Styles", "language": "CSS"},
        ]
    else:
        return [
            {"path": "main.py", "description": "Main entry point", "language": "Python"},
        ]

def create_smart_fallback(idea: str) -> dict:
    """Create a smart fallback plan based on idea analysis."""
    files = detect_files(idea)
    
    return {
        "project_name": "autogenesis-project",
        "description": idea[:100],
        "tech_stack": list(set(f.get("language", "Python") for f in files)),
        "phases": [
            {"name": "Phase 1: Setup", "tasks": ["Initialize project", "Create file structure"]},
            {"name": "Phase 2: Implementation", "tasks": ["Implement core features", "Add styling"]},
            {"name": "Phase 3: Testing", "tasks": ["Test functionality", "Fix bugs"]}
        ],
        "files": files
    }
