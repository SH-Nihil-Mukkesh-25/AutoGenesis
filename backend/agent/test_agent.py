import os
import sys

# Add backend directory to path so we can import 'agent'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent.agent import run_agent

print("Running agent test...")
result = run_agent("A simple todo list app")
print("Result:", result)
