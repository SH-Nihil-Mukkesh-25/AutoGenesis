"""
Advanced Orchestrator with All Features.
Generates: Code, Tests, CI/CD, Deploy configs
"""
from .planner import generate_plan
from .coder import generate_file
from .reviewer import review_code
from .memory import save_memory, get_learning_context
from .intelligence import add_project_xp, get_intelligence
from .capabilities import generate_cicd_pipeline, generate_unit_tests, generate_dockerfile
import os
import json
import shutil

# Improvement prompts for "Build Again But Better"
IMPROVEMENT_INSTRUCTIONS = """
IMPROVEMENT MODE - Generate ENHANCED code with:
1. MORE COMMENTS: Add detailed comments explaining every function and complex logic
2. CLEANER ARCHITECTURE: Use proper design patterns, separation of concerns
3. BETTER PERFORMANCE: Optimize for speed, use efficient algorithms
4. MORE ROBUST: Add error handling, input validation, edge cases
5. PRODUCTION READY: Add logging, type hints, docstrings
"""

def run_pipeline_streaming(idea: str, auto_deploy: bool = False, improve_mode: bool = False):
    """Generator that yields progress updates."""
    def progress(step: str, message: str, percent: int, data: dict = None):
        return json.dumps({
            "step": step,
            "message": message,
            "percent": percent,
            "data": data or {}
        })
    
    mode_label = "IMPROVED" if improve_mode else "standard"
    intel_start = get_intelligence()
    yield progress("start", f"Starting {mode_label} build... (Level {intel_start['level']}%)", 3, {"intelligence": intel_start})
    
    # Clear output folder
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Phase 1: Learning
    yield progress("learning", "Checking context...", 5)
    learning_context = get_learning_context(idea)
    learned = bool(learning_context)
    
    # Phase 2: Planning
    yield progress("planning", "Planning project...", 10)
    plan_idea = idea
    if improve_mode:
        plan_idea = f"{idea}\n\nCREATE AN IMPROVED VERSION with better architecture and more modular design."
    plan = generate_plan(plan_idea)
    files_to_generate = plan.get("files", [{"path": "main.py", "description": "Main"}])
    tech_stack = plan.get("tech_stack", ["Python"])
    yield progress("planning", f"{len(files_to_generate)} files planned", 15, {"plan": plan})
    
    # Phase 3: Generate source files
    generated_files = {}
    languages_used = set()
    total_files = len(files_to_generate)
    
    for i, file_info in enumerate(files_to_generate):
        file_path = file_info.get("path", f"file_{i}.py")
        file_desc = file_info.get("description", "")
        file_lang = file_info.get("language", "Python")
        languages_used.add(file_lang)
        
        file_percent = 20 + int((i / total_files) * 30)
        yield progress("coding", f"Writing {file_path}..." + (" (enhanced)" if improve_mode else ""), file_percent)
        
        other_files = [f["path"] for f in files_to_generate if f["path"] != file_path]
        full_prompt = f"PROJECT: {idea}\nFILE: {file_path}\nPURPOSE: {file_desc}\nLANGUAGE: {file_lang}\nOTHER FILES: {other_files}"
        
        # Add improvement instructions if in improve mode
        if improve_mode:
            full_prompt = IMPROVEMENT_INSTRUCTIONS + "\n\n" + full_prompt
        
        code = generate_file(full_prompt, file_path)
        generated_files[file_path] = code
        
        output_path = os.path.join(output_dir, file_path)
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(code)
    
    yield progress("coding", f"Generated {len(generated_files)} source files", 50)
    
    # Phase 4: Generate Unit Tests
    yield progress("testing", "Generating unit tests...", 55)
    main_file = list(generated_files.keys())[0]
    main_code = generated_files[main_file]
    test_result = generate_unit_tests(main_code, main_file)
    if test_result["content"]:
        generated_files[test_result["path"]] = test_result["content"]
        with open(os.path.join(output_dir, test_result["path"]), "w", encoding="utf-8") as f:
            f.write(test_result["content"])
    yield progress("testing", f"Tests generated: {test_result['path']}", 60)
    
    # Phase 5: Generate CI/CD Pipeline
    yield progress("cicd", "Creating CI/CD pipeline...", 65)
    project_type = "python" if any("Python" in lang for lang in languages_used) else "javascript"
    cicd_result = generate_cicd_pipeline(project_type, list(generated_files.keys()))
    if cicd_result["content"]:
        cicd_path = cicd_result["path"]
        generated_files[cicd_path] = cicd_result["content"]
        full_cicd_path = os.path.join(output_dir, cicd_path)
        os.makedirs(os.path.dirname(full_cicd_path), exist_ok=True)
        with open(full_cicd_path, "w", encoding="utf-8") as f:
            f.write(cicd_result["content"])
    yield progress("cicd", "CI/CD pipeline ready", 70)
    
    # Phase 6: Generate Dockerfile
    yield progress("deploy", "Creating Dockerfile...", 75)
    docker_result = generate_dockerfile(project_type, list(generated_files.keys()))
    if docker_result["content"]:
        generated_files["Dockerfile"] = docker_result["content"]
        with open(os.path.join(output_dir, "Dockerfile"), "w", encoding="utf-8") as f:
            f.write(docker_result["content"])
    yield progress("deploy", "Dockerfile ready", 80)
    
    # Phase 7: Review
    yield progress("reviewing", "Reviewing code...", 85)
    review = review_code(main_code)
    issues_count = len(review.get("issues", []))
    
    # Phase 8: Update Intelligence
    yield progress("learning", "Learning from project...", 90)
    xp_result = add_project_xp(
        files_generated=len(generated_files),
        issues_found=issues_count,
        languages=list(languages_used)
    )
    
    intel_end = get_intelligence()
    yield progress("learning", f"+{xp_result['xp_gained']} XP", 95, {"xp_gained": xp_result["xp_gained"], "intelligence": intel_end})
    
    # Build result
    result = {
        "idea": idea,
        "plan": plan,
        "code_files": list(generated_files.keys()),
        "all_code": generated_files,
        "final_code": "\n\n".join([f"// === {k} ===\n{v}" for k, v in generated_files.items()]),
        "review": review,
        "iterations": [{"iteration": 1, "issues_found": issues_count, "summary": review.get("summary", "")}],
        "total_iterations": 1,
        "deploy": {"success": True, "message": "Dockerfile + CI/CD ready"},
        "learned_from": learned,
        "xp_gained": xp_result["xp_gained"],
        "intelligence": intel_end,
        "extras": {
            "tests": test_result["path"],
            "cicd": cicd_result["path"],
            "dockerfile": "Dockerfile"
        }
    }
    save_memory(result)
    
    yield progress("complete", f"Done! {len(generated_files)} files", 100, result)

def run_pipeline(idea: str, auto_deploy: bool = False, improve_mode: bool = False):
    """Non-streaming version."""
    result = None
    for update in run_pipeline_streaming(idea, auto_deploy, improve_mode):
        data = json.loads(update)
        if data["step"] == "complete":
            result = data["data"]
    return result
