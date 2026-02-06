"""
Configuration module for PRA COREP Reporting Assistant.
"""
import os

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Retrieval Configuration
TOP_K_CHUNKS = 3

# Validation Tolerance (for floating point comparisons)
VALIDATION_TOLERANCE = 0.01
