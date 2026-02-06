"""
Configuration module for PRA COREP Reporting Assistant.
"""
import os

# Gemini API Configuration
def get_gemini_key():
    # 1. Try environment variable
    key = os.getenv("GEMINI_API_KEY", "")
    if key:
        return key
    
    # 2. Try Streamlit secrets (if running in Streamlit)
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except (ImportError, FileNotFoundError, AttributeError):
        pass
        
    return ""

GEMINI_API_KEY = get_gemini_key()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Retrieval Configuration
TOP_K_CHUNKS = 3

# Validation Tolerance (for floating point comparisons)
VALIDATION_TOLERANCE = 0.01
