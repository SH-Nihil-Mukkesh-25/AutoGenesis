"""
Code Generator Module - High quality, language-aware code generation.
"""
from .agent import run_agent
import os

# File extension to language mapping
LANG_MAP = {
    ".py": {"name": "Python", "comment": "#"},
    ".js": {"name": "JavaScript", "comment": "//"},
    ".ts": {"name": "TypeScript", "comment": "//"},
    ".tsx": {"name": "TypeScript React", "comment": "//"},
    ".jsx": {"name": "JavaScript React", "comment": "//"},
    ".html": {"name": "HTML", "comment": "<!--"},
    ".css": {"name": "CSS", "comment": "/*"},
    ".json": {"name": "JSON", "comment": None},
    ".md": {"name": "Markdown", "comment": None},
    ".sql": {"name": "SQL", "comment": "--"},
    ".sh": {"name": "Bash", "comment": "#"},
    ".yaml": {"name": "YAML", "comment": "#"},
    ".yml": {"name": "YAML", "comment": "#"},
}

def get_language_info(filename: str) -> dict:
    """Get language info based on file extension."""
    ext = os.path.splitext(filename)[1].lower()
    return LANG_MAP.get(ext, {"name": "Python", "comment": "#"})

def generate_file(idea: str, filename: str = "main.py") -> str:
    """
    Generates high-quality, language-appropriate code.
    """
    lang = get_language_info(filename)
    lang_name = lang["name"]
    
    prompt = f"""You are an expert {lang_name} developer. Generate production-ready code.

PROJECT IDEA: {idea}

FILE TO CREATE: {filename}
LANGUAGE: {lang_name}

CRITICAL RULES:
1. Generate ONLY valid {lang_name} code for {filename}
2. Do NOT mix languages (no Python in HTML, no HTML in Python, etc.)
3. Include proper imports/dependencies at the top
4. Add clear comments explaining the code
5. Follow best practices for {lang_name}
6. Make the code complete and runnable
7. Handle errors appropriately

{"For HTML: Use proper DOCTYPE, html/head/body structure, link CSS properly" if lang_name == "HTML" else ""}
{"For JavaScript: Use modern ES6+ syntax, handle DOM properly" if "JavaScript" in lang_name else ""}
{"For Python: Use type hints, docstrings, and if __name__ == '__main__'" if lang_name == "Python" else ""}
{"For CSS: Use modern CSS, proper selectors, responsive design" if lang_name == "CSS" else ""}

Return ONLY the {lang_name} code. No markdown, no explanations, no code fences."""

    result = run_agent(prompt, mode="code")
    
    code = ""
    if "code" in result:
        code = result["code"]
    elif "response" in result:
        code = result["response"]
    
    # Clean up any markdown artifacts
    code = clean_code(code, lang_name)
    
    return code

def clean_code(code: str, language: str) -> str:
    """Remove markdown artifacts, prompts, and clean the code."""
    import re
    
    # First try to extract from markdown code block
    if "```" in code:
        match = re.search(r'```\w*\n([\s\S]*?)```', code)
        if match:
            code = match.group(1)
        else:
            # Fallback: remove code fence lines
            lines = code.split("\n")
            code = "\n".join(l for l in lines if not l.strip().startswith("```"))
    
    lines = code.strip().split("\n")
    cleaned = []
    
    # Lines that indicate prompt leakage (skip these)
    skip_patterns = [
        "# Idea:",
        "# Autogenesis Generated",
        "# PROJECT:",
        "# FILE TO CREATE:",
        "# LANGUAGE:",
        "# CRITICAL RULES:",
        "You are an expert",
        "Generate production-ready",
        "Return ONLY",
    ]
    
    for line in lines:
        # Skip lines that look like prompts
        skip = False
        for pattern in skip_patterns:
            if pattern in line:
                skip = True
                break
        
        if not skip:
            cleaned.append(line)
    
    result = "\n".join(cleaned).strip()
    
    # If result is empty or just whitespace, return template
    if not result or len(result) < 5:
        return get_template(language)
    
    return result

def get_template(language: str) -> str:
    """Return a basic template for a language."""
    templates = {
        "Python": '''"""
Auto-generated Python module.
"""

def main():
    """Main entry point."""
    print("Hello from Autogenesis!")

if __name__ == "__main__":
    main()
''',
        "JavaScript": '''/**
 * Auto-generated JavaScript module.
 */

function main() {
    console.log("Hello from Autogenesis!");
}

main();
''',
        "HTML": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autogenesis Project</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Hello from Autogenesis!</h1>
    <script src="main.js"></script>
</body>
</html>
''',
        "CSS": '''/* Modern CSS Reset and Base Styles */
:root {
    --primary: #6366f1;
    --bg: #0f0f0f;
    --surface: #1a1a1a;
    --text: #ffffff;
    --text-muted: #a1a1aa;
    --border: #27272a;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

button {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    font-size: 1rem;
    transition: opacity 0.2s;
}

button:hover {
    opacity: 0.9;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 1.5rem;
}
''',
    }
    return templates.get(language, "# Auto-generated file\n")

def fix_code(code: str, issues: list, idea: str = "", filename: str = "main.py") -> str:
    """Fix code issues while respecting the file's language."""
    if not issues:
        return code
    
    lang = get_language_info(filename)
    lang_name = lang["name"]
    
    issues_text = "\n".join(f"- {issue}" for issue in issues)
    prompt = f"""You are an expert {lang_name} developer. Fix the following code.

FILE: {filename}
LANGUAGE: {lang_name}

ISSUES TO FIX:
{issues_text}

CURRENT CODE:
{code}

CRITICAL: Return ONLY valid {lang_name} code. No markdown, no explanations."""
    
    result = run_agent(prompt, mode="code")
    
    if "code" in result:
        return clean_code(result["code"], lang_name)
    elif "response" in result:
        return clean_code(result["response"], lang_name)
    
    return code
