import os
import sys
from google import genai

os.environ["GEMINI_API_KEY"] = "AIzaSyDpN3J8EFALudJa_t9HPW3XDo6Bh7u5oR8"
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("Listing models...")
try:
    for m in client.models.list():
        print(f"Model: {m.name}")
        # print(f"Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Listing failed: {e}")
