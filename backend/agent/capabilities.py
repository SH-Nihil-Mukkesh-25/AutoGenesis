"""
Advanced Agent Capabilities - Auto-fix, CI/CD, Tests, Deploy
"""
from .agent import run_agent
import os

def generate_cicd_pipeline(project_type: str, files: list) -> dict:
    """Generate CI/CD pipeline configuration based on project type."""
    prompt = f"""Generate a GitHub Actions CI/CD pipeline for this project.

Project type: {project_type}
Files: {files}

Create a complete .github/workflows/main.yml file that:
1. Runs on push and pull requests
2. Sets up the correct environment
3. Installs dependencies
4. Runs tests
5. Builds the project
6. Deploys if on main branch

Return ONLY the YAML content, no markdown."""

    result = run_agent(prompt, mode="code")
    yaml_content = result.get("code") or result.get("response", "")
    
    # Clean markdown
    if "```" in yaml_content:
        lines = yaml_content.split("\n")
        yaml_content = "\n".join(l for l in lines if not l.strip().startswith("```"))
    
    return {
        "path": ".github/workflows/main.yml",
        "content": yaml_content.strip(),
        "type": "cicd"
    }

def generate_unit_tests(code: str, filename: str) -> dict:
    """Generate unit tests for the given code."""
    prompt = f"""Generate comprehensive unit tests for this code.

FILE: {filename}
CODE:
{code}

Create proper unit tests that:
1. Test all functions
2. Include edge cases
3. Use appropriate testing framework (pytest for Python, Jest for JS)
4. Have clear test names

Return ONLY the test code, no markdown."""

    result = run_agent(prompt, mode="code")
    test_content = result.get("code") or result.get("response", "")
    
    if "```" in test_content:
        lines = test_content.split("\n")
        test_content = "\n".join(l for l in lines if not l.strip().startswith("```"))
    
    # Generate test filename
    base = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    test_filename = f"test_{base}{ext}"
    
    return {
        "path": test_filename,
        "content": test_content.strip(),
        "type": "test"
    }

def auto_fix_code(code: str, error_message: str = "") -> dict:
    """Fix ALL errors in code and improve quality."""
    prompt = f"""You are an expert code fixer. Fix ALL issues in this code and improve its quality.

CURRENT CODE:
{code}

{f"KNOWN ISSUES: {error_message}" if error_message else ""}

YOUR TASK:
1. Fix ALL syntax errors
2. Fix ALL logic errors  
3. Fix ALL typos
4. Add proper error handling
5. Add helpful comments
6. Improve code structure
7. Make it production-ready
8. Ensure it actually works

IMPORTANT: Return ONLY the complete fixed code. No explanations, no markdown, just pure code.
The code must be complete and ready to run."""

    result = run_agent(prompt, mode="code")
    fixed_code = result.get("code") or result.get("response", "")
    
    # Clean markdown artifacts
    if "```" in fixed_code:
        import re
        # Extract code between markdown blocks
        match = re.search(r'```\w*\n([\s\S]*?)```', fixed_code)
        if match:
            fixed_code = match.group(1)
        else:
            lines = fixed_code.split("\n")
            fixed_code = "\n".join(l for l in lines if not l.strip().startswith("```"))
    
    # Remove any "# Autogenesis Generated" headers
    if fixed_code.startswith("# Autogenesis"):
        lines = fixed_code.split("\n")
        fixed_code = "\n".join(lines[1:])
    
    return {
        "fixed_code": fixed_code.strip(),
        "type": "fix"
    }

def generate_dockerfile(project_type: str, files: list) -> dict:
    """Generate Dockerfile for deployment."""
    prompt = f"""Generate a production-ready Dockerfile.

Project type: {project_type}
Files: {files}

Create a Dockerfile that:
1. Uses appropriate base image
2. Installs dependencies efficiently
3. Copies source code
4. Exposes correct ports
5. Has proper CMD/ENTRYPOINT

Return ONLY the Dockerfile content, no markdown."""

    result = run_agent(prompt, mode="code")
    dockerfile = result.get("code") or result.get("response", "")
    
    if "```" in dockerfile:
        lines = dockerfile.split("\n")
        dockerfile = "\n".join(l for l in lines if not l.strip().startswith("```"))
    
    return {
        "path": "Dockerfile",
        "content": dockerfile.strip(),
        "type": "deploy"
    }

def generate_vercel_config(project_type: str) -> dict:
    """Generate Vercel deployment config."""
    configs = {
        "static": '{"buildCommand": "", "outputDirectory": "."}',
        "next": '{"framework": "nextjs"}',
        "react": '{"framework": "create-react-app"}',
        "python": '{"builds": [{"src": "api/*.py", "use": "@vercel/python"}]}'
    }
    
    return {
        "path": "vercel.json",
        "content": configs.get(project_type, configs["static"]),
        "type": "deploy"
    }
