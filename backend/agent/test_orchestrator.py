from agent.orchestrator import run_pipeline
from agent.memory import read_memory
import shutil

# Clean previous output
try:
    shutil.rmtree("output")
except:
    pass

print("Testing Orchestrator...")
result = run_pipeline("Create a simple calculator")
print("Pipeline Result Keys:", result.keys())

memory = read_memory()
print(f"Memory count: {len(memory)}")

if "plan" in result and "code_files" in result and "review" in result:
    print("SUCCESS: Pipeline returned full structure")
else:
    print("FAILURE: Pipeline structure missing keys. Got:", result.keys())

import os
if os.path.exists("output/main.py"):
    print("SUCCESS: Output file created")
else:
    print("FAILURE: Output file not created")
