
import os
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

print(f"GROQ_KEY Length: {len(groq_key) if groq_key else 0}")
print(f"GEMINI_KEY Length: {len(gemini_key) if gemini_key else 0}")

if groq_key:
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        print("Attempting Groq request...")
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10
        )
        print(f"Groq Success: {resp.choices[0].message.content}")
    except Exception as e:
        print(f"Groq FAILED: {type(e).__name__}: {e}")

if gemini_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        print("Attempting Gemini request...")
        model = genai.GenerativeModel("gemini-2.0-flash")
        resp = model.generate_content("Say 'Hello'")
        print(f"Gemini Success: {resp.text}")
    except Exception as e:
        print(f"Gemini FAILED: {type(e).__name__}: {e}")
