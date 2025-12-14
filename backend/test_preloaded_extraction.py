
from agent.agent import run_agent
from agent.coder import generate_file

# Simulate the exact prompt structure from coder.py
# We can't import the template string easily, so we reconstruct it based on reading coder.py
# Reference coder.py lines 36-57

def test_extraction():
    idea = "Build a calculator"
    filename = "index.html"
    lang_name = "HTML"
    
    # This is the prompt constructed in coder.py
    prompt = f"""You are an expert {lang_name} developer. Generate production-ready code.

PROJECT IDEA: {idea}

FILE TO CREATE: {filename}
LANGUAGE: {lang_name}

CRITICAL RULES:
1. Generate ONLY valid {lang_name} code for {filename}
...
"""
    
    print(f"--- Simulating run_agent with prompt for {filename} ---")
    
    # We call run_agent directly with mode="code" and the constructed prompt
    # This mimics what happens inside generate_file -> run_agent
    result = run_agent(prompt, mode="code")
    
    if "code" in result and "<!DOCTYPE html>" in result["code"]:
        print("✅ SUCCESS: Extracted filename and returned preloaded HTML")
    else:
        print("❌ FAILURE: Did not return preloaded HTML")
        print(f"Result keys: {result.keys()}")
        if "response" in result:
             print(f"Response snippet: {result['response'][:50]}...")

if __name__ == "__main__":
    test_extraction()
