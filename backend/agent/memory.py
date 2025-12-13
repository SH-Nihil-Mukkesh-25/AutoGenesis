import json
from pathlib import Path

MEMORY_FILE = Path("storage/memory.json")

def save_memory(data):
    """
    Saves data to memory.json.
    """
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    
    current_memory = []
    if MEMORY_FILE.exists():
        try:
             current_memory = json.loads(MEMORY_FILE.read_text())
        except:
             pass
    
    current_memory.append(data)
    MEMORY_FILE.write_text(json.dumps(current_memory, indent=2))

def read_memory():
    """
    Reads all memory.
    """
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except:
            return []
    return []

def get_similar_projects(idea: str, limit: int = 3):
    """
    Find past projects similar to the current idea.
    Uses simple keyword matching for now.
    """
    memory = read_memory()
    if not memory:
        return []
    
    # Simple relevance scoring based on word overlap
    idea_words = set(idea.lower().split())
    scored = []
    
    for project in memory:
        past_idea = project.get("idea", "")
        past_words = set(past_idea.lower().split())
        overlap = len(idea_words & past_words)
        if overlap > 0:
            scored.append((overlap, project))
    
    # Sort by overlap score descending
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:limit]]

def get_learning_context(idea: str):
    """
    Generate context from past projects to improve new generations.
    """
    similar = get_similar_projects(idea)
    if not similar:
        return ""
    
    context = "Based on similar past projects, here's what worked:\n"
    for p in similar:
        context += f"- For '{p.get('idea', '')}', we generated: {p.get('code_files', [])}\n"
        if p.get('review', {}).get('issues'):
            context += f"  Issues to avoid: {p['review']['issues']}\n"
    
    return context

def get_memory_history():
    """
    Get formatted project history for Memory View.
    Returns list of projects with key metrics.
    """
    from datetime import datetime
    memory = read_memory()
    
    history = []
    for i, project in enumerate(memory):
        # Extract info
        idea = project.get("idea", "Unknown project")
        xp = project.get("xp_gained", 0)
        files = project.get("code_files", [])
        
        # Get languages from plan
        plan = project.get("plan", {})
        tech = plan.get("tech_stack", [])
        if not tech:
            # Infer from files
            for f in files:
                if f.endswith(".py"):
                    tech.append("Python")
                elif f.endswith(".html"):
                    tech.append("HTML")
                elif f.endswith(".css"):
                    tech.append("CSS")
                elif f.endswith(".js"):
                    tech.append("JavaScript")
            tech = list(set(tech))
        
        history.append({
            "id": i + 1,
            "idea": idea[:60] + ("..." if len(idea) > 60 else ""),
            "xp_gained": xp,
            "languages": tech[:3],  # Max 3 languages
            "file_count": len(files),
            "files": files[:5],  # Max 5 files shown
            "quality_score": project.get("review", {}).get("score", 8),
            "timestamp": project.get("timestamp", datetime.now().isoformat()[:10])
        })
    
    # Most recent first
    history.reverse()
    return history[:20]  # Last 20 projects
