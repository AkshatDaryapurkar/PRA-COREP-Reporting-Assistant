import os
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = "AIzaSyDpN3J8EFALudJa_t9HPW3XDo6Bh7u5oR8"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print(f"Version: {genai.__version__}")

models_to_try = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-pro",
    "gemini-1.0-pro"
]

for model_name in models_to_try:
    print(f"\nTesting {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi")
        print(f"SUCCESS: {response.text}")
        break
    except Exception as e:
        print(f"FAILED: {e}")
