import os
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = "AIzaSyDpN3J8EFALudJa_t9HPW3XDo6Bh7u5oR8"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("--- START MODEL LIST ---")
try:
    for m in genai.list_models():
        print(f"Model: {m.name}")
        print(f"Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Listing failed: {e}")
print("--- END MODEL LIST ---")
