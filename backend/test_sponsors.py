try:
    import oumi
    print("SUCCESS: Oumi imported")
except ImportError as e:
    print(f"WARNING: Oumi import failed (likely build tools missing): {e}")

import os
required_files = [
    "../kestra/flows/summarize_memory.yaml",
    "../vercel.json",
    "../.coderabbit.yaml",
    "training/train_reasoner.py"
]

for f in required_files:
    if os.path.exists(f):
        print(f"SUCCESS: Found {f}")
    else:
        print(f"FAILURE: Missing {f}")
