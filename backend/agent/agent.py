"""
Autogenesis AI Agent - Supports Groq API (primary) with Gemini fallback.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Check for Groq API key first, then Gemini
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# Determine which provider to use
USE_GROQ = GROQ_API_KEY is not None
USE_GEMINI = GEMINI_API_KEY is not None and not USE_GROQ

if USE_GROQ:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    print("🚀 Using Groq API (llama-3.3-70b-versatile)")
elif USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    print("🚀 Using Gemini API")
else:
    if not MOCK_MODE:
        print("⚠️ No API key found! Set GROQ_API_KEY or GEMINI_API_KEY in .env, or enable MOCK_MODE=true")

# Track rate limit state
_rate_limited = False

def is_rate_limited():
    """Check if currently rate limited."""
    return _rate_limited

def run_agent(idea: str, mode: str = "plan"):
    """
    Main agent function - routes to appropriate AI provider.
    Returns response with rate_limited flag when applicable.
    """
    global _rate_limited
    
    if MOCK_MODE:
        _rate_limited = False
        return mock_response(idea, mode)
    
    if USE_GROQ:
        result = groq_request(idea, mode)
        # Check if it fell back to mock (rate limited)
        if result.get("_mock_fallback"):
            _rate_limited = True
            del result["_mock_fallback"]
        else:
            _rate_limited = False
        return result
    elif USE_GEMINI:
        return gemini_request(idea, mode)
    else:
        return mock_response(idea, mode)

def mock_response(idea: str, mode: str):
    """Language-aware mock responses with unique content per project."""
    idea_lower = idea.lower()
    
    # Determine project type
    is_web = any(w in idea_lower for w in ["web", "website", "html", "landing", "portfolio", "page", "chatbot", "calculator", "todo", "ui"])
    is_api = any(w in idea_lower for w in ["api", "flask", "backend", "rest", "server", "crud"])
    is_react = any(w in idea_lower for w in ["react", "next", "component", "dashboard", "saas"])
    
    if mode == "plan":
        if is_web:
            files = [
                {"path": "index.html", "description": "Main HTML page", "language": "HTML"},
                {"path": "styles.css", "description": "Stylesheet", "language": "CSS"},
                {"path": "main.js", "description": "JavaScript logic", "language": "JavaScript"},
            ]
            tech = ["HTML", "CSS", "JavaScript"]
        elif is_api:
            files = [
                {"path": "app.py", "description": "Flask server", "language": "Python"},
                {"path": "routes.py", "description": "API routes", "language": "Python"},
            ]
            tech = ["Python", "Flask"]
        elif is_react:
            files = [
                {"path": "App.tsx", "description": "Main component", "language": "TypeScript"},
                {"path": "index.tsx", "description": "Entry", "language": "TypeScript"},
                {"path": "styles.css", "description": "Styles", "language": "CSS"},
            ]
            tech = ["React", "TypeScript"]
        else:
            files = [{"path": "main.py", "description": "Main module", "language": "Python"}]
            tech = ["Python"]
        
        return {
            "project_name": "autogenesis-project",
            "description": idea[:80],
            "tech_stack": tech,
            "phases": [
                {"name": "Phase 1: Setup", "tasks": ["Initialize project"]},
                {"name": "Phase 2: Build", "tasks": ["Implement features"]},
            ],
            "files": files
        }
    
    elif mode == "code":
        # Extract filename from prompt
        filename = ""
        for line in idea.split("\n"):
            if "FILE:" in line:
                filename = line.split("FILE:")[-1].strip()
                break
        
        # Detect project theme from idea for unique content
        title = "Welcome"
        if "portfolio" in idea_lower:
            title = "My Portfolio"
        elif "landing" in idea_lower:
            title = "Launch Your Product"
        elif "chatbot" in idea_lower:
            title = "AI Assistant"
        elif "calculator" in idea_lower:
            title = "Calculator"
        elif "todo" in idea_lower:
            title = "Task Manager"
        elif "crud" in idea_lower:
            title = "Data Manager"
        
        # Return appropriate code based on filename
        if filename.endswith(".css"):
            primary = "#6366f1" if "portfolio" not in idea_lower else "#10b981"
            return {"code": f"""/* Generated Styles */
:root {{
    --primary: {primary};
    --bg: #0a0a0a;
    --surface: #141414;
    --text: #fff;
    --muted: #888;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Inter', -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
}}
.container {{
    max-width: 1000px;
    margin: 0 auto;
    padding: 3rem 2rem;
}}
h1 {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--primary), #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
p {{ color: var(--muted); margin-bottom: 2rem; }}
button {{
    background: var(--primary);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 0.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: transform 0.2s;
}}
button:hover {{ transform: translateY(-2px); }}
.card {{
    background: var(--surface);
    border: 1px solid #222;
    border-radius: 1rem;
    padding: 2rem;
    margin-top: 2rem;
}}
"""}
        elif filename.endswith(".html"):
            return {"code": f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p>Built with Autogenesis - AI-powered code generation</p>
        <button id="main-btn">Get Started</button>
        <div class="card">
            <h3>Features</h3>
            <ul style="color: #888; margin-top: 1rem; padding-left: 1.5rem;">
                <li>Fast and responsive</li>
                <li>Modern design</li>
                <li>Easy to customize</li>
            </ul>
        </div>
    </div>
    <script src="main.js"></script>
</body>
</html>"""}
        elif filename.endswith(".js"):
            return {"code": f"""// {title} - JavaScript
document.addEventListener('DOMContentLoaded', () => {{
    console.log('{title} initialized');
    
    const btn = document.getElementById('main-btn');
    if (btn) {{
        btn.addEventListener('click', () => {{
            btn.textContent = 'Loading...';
            setTimeout(() => {{
                btn.textContent = 'Done!';
                btn.style.background = '#10b981';
            }}, 1000);
        }});
    }}
}});
"""}
        else:
            return {"code": f'''"""{title} - Main Module"""

def main():
    """Entry point."""
    print("{title} started!")
    run_app()

def run_app():
    """Core application logic."""
    print("Running...")

if __name__ == "__main__":
    main()
'''}
    
    elif mode == "review":
        return {"has_errors": False, "errors": [], "summary": "Code looks good!", "score": 9}
    
    return {"response": idea}

def groq_request(idea: str, mode: str):
    """Use Groq API (llama-3.3-70b-versatile)."""
    try:
        if mode == "plan":
            prompt = f"""You are an AI software architect. Create a structured project plan for this idea: {idea}

Return ONLY valid JSON with this structure:
{{"phases": [{{"name": "Phase 1: ...", "tasks": ["task1", "task2"]}}]}}"""
        elif mode == "code":
            prompt = f"""You are an expert developer. Generate clean, working Python code for: {idea}

Return ONLY the code, no markdown or explanations."""
        elif mode == "review":
            prompt = f"""You are an expert code reviewer. Review this code and return JSON:
{{"issues": ["issue1"], "summary": "Brief summary"}}

Code to review:
{idea}"""
        else:
            prompt = f"Help with: {idea}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048
        )
        
        content = response.choices[0].message.content
        
        # Try to parse as JSON for plan/review modes
        if mode in ["plan", "review"]:
            import json
            try:
                # Find JSON in response
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    return json.loads(content[start:end])
            except:
                pass
        
        if mode == "code":
            # Clean markdown if present
            if "```" in content:
                lines = content.split("\n")
                code_lines = []
                in_code = False
                for line in lines:
                    if line.startswith("```"):
                        in_code = not in_code
                        continue
                    if in_code:
                        code_lines.append(line)
                return {"code": "\n".join(code_lines) if code_lines else content}
            return {"code": content}
        
        return {"response": content}
        
    except Exception as e:
        print(f"Groq API error: {e}")
        result = mock_response(idea, mode)
        result["_mock_fallback"] = True  # Flag for rate limit tracking
        return result

def gemini_request(idea: str, mode: str):
    """Use Gemini API with fallback to mock on 429."""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        if mode == "plan":
            prompt = f"You are an AI software architect. Create a structured project plan (JSON) for: {idea}. Return ONLY valid JSON with 'phases' list."
        elif mode == "code":
            prompt = f"You are an expert developer. Generate code for: {idea}. Return ONLY the code."
        elif mode == "review":
            prompt = f"Review this code and return JSON with 'issues' and 'summary': {idea}"
        else:
            prompt = f"Help with: {idea}"

        response = model.generate_content(prompt)
        return {"response": response.text}
        
    except Exception as e:
        if "429" in str(e):
            print(f"Gemini quota exceeded, using mock: {e}")
            return mock_response(idea, mode)
        return {"error": str(e)}
