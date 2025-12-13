"""
Enhanced Code Reviewer with Error Detection.
Returns structured error info with line numbers and explanations.
"""
from .agent import run_agent
import re

def review_code(code: str) -> dict:
    """
    Reviews code and returns detailed error analysis.
    """
    prompt = f"""Analyze this code for errors and issues.

CODE:
{code}

Return a JSON object with this EXACT structure:
{{
    "has_errors": true/false,
    "errors": [
        {{
            "line": <line_number>,
            "code_snippet": "<the problematic code>",
            "error_type": "<SyntaxError/TypeError/LogicError/etc>",
            "message": "<what's wrong>",
            "explanation": "<why this is wrong and how to understand it>",
            "fix": "<the corrected code snippet>"
        }}
    ],
    "summary": "<overall code quality summary>",
    "score": <1-10 quality score>
}}

If no errors, return has_errors: false with empty errors array.
Return ONLY valid JSON, no markdown."""

    result = run_agent(prompt, mode="review")
    
    # Try to parse structured response
    if "errors" in result:
        return result
    elif "response" in result:
        # Try to parse JSON from response
        try:
            import json
            text = result["response"]
            # Clean markdown
            if "```" in text:
                text = re.sub(r'```json?\s*', '', text)
                text = re.sub(r'```\s*', '', text)
            parsed = json.loads(text.strip())
            return parsed
        except:
            pass
    
    # Fallback: basic analysis
    return analyze_code_basic(code)

def analyze_code_basic(code: str) -> dict:
    """
    Basic static analysis fallback.
    """
    errors = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Check for common issues
        stripped = line.strip()
        
        # Missing colons in Python
        if re.match(r'^(def|class|if|elif|else|for|while|try|except|with)\s+.*[^:]$', stripped):
            if not stripped.endswith(':') and not stripped.endswith(','):
                errors.append({
                    "line": i,
                    "code_snippet": line,
                    "error_type": "SyntaxError",
                    "message": "Missing colon at end of statement",
                    "explanation": "In Python, compound statements like 'def', 'if', 'for' must end with a colon (:)",
                    "fix": line.rstrip() + ":"
                })
        
        # Unclosed parentheses (simple check)
        if line.count('(') != line.count(')'):
            errors.append({
                "line": i,
                "code_snippet": line,
                "error_type": "SyntaxError",
                "message": "Unbalanced parentheses",
                "explanation": "The number of opening and closing parentheses don't match on this line",
                "fix": None
            })
        
        # console.log typo in Python
        if 'console.log' in line and '.py' in str(code[:50]):
            errors.append({
                "line": i,
                "code_snippet": line,
                "error_type": "TypeError",
                "message": "console.log is JavaScript, not Python",
                "explanation": "In Python, use print() instead of console.log()",
                "fix": line.replace('console.log', 'print')
            })
    
    return {
        "has_errors": len(errors) > 0,
        "errors": errors,
        "summary": f"Found {len(errors)} potential issue(s)" if errors else "No obvious errors detected",
        "score": max(1, 10 - len(errors) * 2)
    }

def get_error_for_line(review_result: dict, line_num: int) -> dict:
    """Get error info for a specific line."""
    for error in review_result.get("errors", []):
        if error.get("line") == line_num:
            return error
    return None
