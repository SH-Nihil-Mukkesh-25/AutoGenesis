from agent.coder import generate_file

print("Testing Coder...")
code = generate_file("hello.py", "A simple hello world script")
print("Generated Code:\n", code)

if "def main" in code or "print" in code:
    print("SUCCESS: Code generated")
else:
    print("FAILURE: Code generation failed")
