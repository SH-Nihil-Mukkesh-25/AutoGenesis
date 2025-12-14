from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from agent.orchestrator import run_pipeline, run_pipeline_streaming

import shutil
import os

# -------------------------------
# MODELS
# -------------------------------
class Prompt(BaseModel):
    idea: str
    improve: bool = False



# -------------------------------
# APP INSTANCE
# -------------------------------
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OptimizeRequest(BaseModel):
    idea: str

@app.post("/optimize")
async def optimize_prompt(req: OptimizeRequest):
    """Optimize the user's prompt using AI."""
    from agent.agent import run_agent
    result = run_agent(req.idea, mode="optimize")
    return {"optimized_prompt": result.get("response", req.idea)}

# -------------------------------
# ROUTES
# -------------------------------

@app.get("/")
async def root():
    return {"status": "Autogenesis Backend Running", "endpoints": ["/run", "/run-stream", "/export", "/templates", "/ping"]}

@app.get("/templates")
async def get_templates():
    """Get available project templates."""
    from agent.templates import get_templates
    return get_templates()

@app.get("/memory")
async def get_memory():
    """Get project history for Memory View."""
    from agent.memory import get_memory_history
    return get_memory_history()

@app.post("/run")
async def run(prompt: Prompt):
    """Standard endpoint - returns final result only."""
    result = run_pipeline(prompt.idea, improve_mode=prompt.improve)
    return {"result": result}

@app.post("/run-stream")
async def run_stream(prompt: Prompt):
    """SSE streaming endpoint - yields progress updates."""
    def generate():
        for update in run_pipeline_streaming(prompt.idea, improve_mode=prompt.improve):
            yield f"data: {update}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.get("/export")
async def export_project():
    """Zips the output directory and returns it."""
    output_dir = "output"
    if not os.path.exists(output_dir):
        return {"error": "No project generated yet."}

    shutil.make_archive("project", 'zip', output_dir)
    return FileResponse(
        "project.zip",
        media_type="application/zip",
        filename="autogenesis_project.zip"
    )

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/intelligence")
async def get_intel():
    """Get current AI intelligence/growth stats."""
    from agent.intelligence import get_intelligence
    return get_intelligence()

@app.get("/skills")
async def get_skills():
    """Get skill tree data."""
    from agent.intelligence import get_intelligence
    from agent.skills import get_skill_tree_data
    intel = get_intelligence()
    return get_skill_tree_data(intel["level"])

class FixRequest(BaseModel):
    code: str
    error: str = ""

@app.post("/fix")
async def auto_fix(req: FixRequest):
    """Auto-fix code based on error."""
    from agent.capabilities import auto_fix_code
    result = auto_fix_code(req.code, req.error)
    return result

@app.get("/status")
async def get_status():
    """Get API status including rate limit state."""
    from agent.agent import is_rate_limited, USE_GROQ, USE_GEMINI, MOCK_MODE
    return {
        "rate_limited": is_rate_limited(),
        "provider": "groq" if USE_GROQ else "gemini" if USE_GEMINI else "mock",
        "mock_mode": MOCK_MODE,
        "env_check": {
            "GROQ": bool(os.getenv("GROQ_API_KEY")),
            "GEMINI": bool(os.getenv("GEMINI_API_KEY"))
        }
    }

@app.get("/debug")
async def debug_agent():
    """Debug endpoint to check preloaded logic and env."""
    from agent.preloaded import get_preloaded_project
    calc_demo = get_preloaded_project("calculator")
    return {
        "preloaded_check": "SUCCESS" if calc_demo else "FAILED",
        "demo_name": calc_demo.get("project_name") if calc_demo else None,
        "env": os.environ.copy() # CAUTION: Don't show this in prod usually, but needed for debug now
    }

class ExplainRequest(BaseModel):
    code: str
    language: str = "Python"

@app.post("/explain")
async def explain_code(req: ExplainRequest):
    """Get AI explanation of code."""
    from agent.agent import run_agent
    prompt = f"""Explain this {req.language} code line by line in simple terms.
Be concise. Format as a list of explanations.

CODE:
{req.code}

Return JSON: {{"explanations": [{{"line": 1, "code": "...", "explanation": "..."}}]}}"""
    
    result = run_agent(prompt, mode="review")
    
    # Parse or fallback
    if "explanations" in result:
        return result
    
    # Generate simple fallback
    lines = req.code.strip().split("\n")
    explanations = []
    for i, line in enumerate(lines[:10], 1):  # Max 10 lines
        if line.strip():
            explanations.append({
                "line": i,
                "code": line[:50],
                "explanation": f"Line {i}: {line.strip()[:30]}..."
            })
    return {"explanations": explanations}

class DeployRequest(BaseModel):
    project_name: str = "autogenesis-project"

@app.delete("/reset")
async def reset_demo():
    """RESET ENDPOINT FOR DEMO: Wipes all memory and intelligence."""
    
    deleted = []
    
    # Files to delete
    params = [
        "storage/memory.json",
        "storage/intelligence.json"
    ]
    
    for p in params:
        try:
            if os.path.exists(p):
                os.remove(p)
                deleted.append(p)
        except Exception as e:
            return {"error": f"Failed to delete {p}: {str(e)}"}
            
    # Also clear output folder
    if os.path.exists("output"):
        shutil.rmtree("output")
        deleted.append("output/")

    return {
        "success": True, 
        "message": "Demo state reset successfully! Reload frontend to see 0% state.",
        "deleted": deleted
    }

@app.post("/deploy")
async def deploy_to_vercel(req: DeployRequest):
    """Simulate Vercel deployment (returns deployment URL)."""
    import random
    import string
    
    # Generate mock deployment ID
    deploy_id = ''.join(random.choices(string.ascii_lowercase, k=8))
    
    return {
        "success": True,
        "url": f"https://{req.project_name}-{deploy_id}.vercel.app",
        "message": "Deployed successfully! (Demo mode - install Vercel CLI for real deployments)",
        "deploy_id": deploy_id
    }
