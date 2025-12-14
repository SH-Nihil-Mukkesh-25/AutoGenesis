
import sys
import os
sys.path.append(os.getcwd()) # Add backend to path

from agent.agent import run_agent

print("Testing run_agent with simple idea...")
try:
    result = run_agent("Build a simple HTML button", mode="code")
    print("RESULT KEYS:", result.keys())
    if "code" in result:
        print("CODE START:", result["code"][:50])
    
    # Check if logic fell back to mock matches known mock pattern
    if "Built with Autogenesis" in str(result):
        print("⚠️ FALLBACK TO MOCK DETECTED")
    else:
        print("✅ SUCCESS (Real AI Response)")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
