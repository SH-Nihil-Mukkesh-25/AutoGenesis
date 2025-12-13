from agent.reviewer import review_code

print("Testing Reviewer...")
code = "def main(): print('hello')"
result = review_code(code)
print("Review Result:", result)

if "issues" in result and "summary" in result:
    print("SUCCESS: Review generated")
else:
    print("FAILURE: Review structure incorrect")
