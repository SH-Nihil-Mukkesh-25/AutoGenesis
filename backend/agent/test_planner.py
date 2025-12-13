import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent.planner import generate_plan
from agent.agent import MOCK_MODE

print(f"Testing Planner (Mock Mode: {MOCK_MODE})...")
plan = generate_plan("Build a simple blog")
print("Plan Output:", plan)

if "phases" in plan:
    print("SUCCESS: Plan has 'phases'")
else:
    print("FAILURE: Plan missing 'phases'")
