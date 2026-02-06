import os
import google.generativeai as genai

# Use the key from config (simulated here)
os.environ["GEMINI_API_KEY"] = "AIzaSyDpN3J8EFALudJa_t9HPW3XDo6Bh7u5oR8"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("Listing models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")

print("\nTesting generation with 'gemini-1.5-flash'...")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, can you reply with 'Working'?")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error with 'gemini-1.5-flash': {e}")
    
    print("\nTesting generation with 'models/gemini-1.5-flash'...")
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content("Hello, can you reply with 'Working'?")
        print(f"Response: {response.text}")
    except Exception as e2:
        print(f"Error with 'models/gemini-1.5-flash': {e2}")
