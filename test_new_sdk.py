import os
import sys

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("google-genai not installed")
    sys.exit(1)

os.environ["GEMINI_API_KEY"] = "AIzaSyDpN3J8EFALudJa_t9HPW3XDo6Bh7u5oR8"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("Testing with google-genai SDK...")
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hello"
    )
    print(f"SUCCESS: {response.text}")
except Exception as e:
    print(f"FAILED: {e}")
