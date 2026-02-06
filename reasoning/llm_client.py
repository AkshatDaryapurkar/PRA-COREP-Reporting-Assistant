"""
LLM client abstraction for Google Gemini API (google-genai SDK).
"""
import json
import re
from typing import Optional

from google import genai
from google.genai import types

import config


class LLMClient:
    """Abstracted LLM client supporting Google Gemini API via google-genai SDK."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize with API key and model."""
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model_name = model or config.GEMINI_MODEL
        self._client = None
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not set. "
                "Set GEMINI_API_KEY environment variable."
            )
    
    @property
    def client(self) -> genai.Client:
        """Lazy load Gemini client."""
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client
    
    def generate_response(
        self, 
        system_prompt: str, 
        user_prompt: str,
        temperature: float = 0.1
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            system_prompt: System instructions
            user_prompt: User message with context
            temperature: Sampling temperature
            
        Returns:
            Raw response text from LLM
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            raise
    
    def generate_json(
        self, 
        system_prompt: str, 
        user_prompt: str,
        temperature: float = 0.1
    ) -> Optional[dict]:
        """
        Generate and parse JSON response from LLM.
        
        Args:
            system_prompt: System instructions
            user_prompt: User message with context
            temperature: Sampling temperature
            
        Returns:
            Parsed JSON dict or None if parsing fails
        """
        # Append JSON instruction to ensure format
        json_instruction = (
            "\n\nIMPORTANT: Output ONLY valid JSON code. "
            "Do not include any other text."
        )
        full_user_prompt = user_prompt + json_instruction
        
        try:
            # We can use response_mime_type with newer models, but sticking to prompt eng for safety
            # Actually, google-genai makes it easy to enforce JSON:
            # config=types.GenerateContentConfig(response_mime_type="application/json")
            # But let's keep it simple and consistent with previous logic for now.
            
            response_text = self.generate_response(system_prompt, full_user_prompt, temperature)
            return self._extract_json(response_text)
        except Exception as e:
            print(f"Error generating JSON: {e}")
            return None
    
    @staticmethod
    def _extract_json(text: str) -> Optional[dict]:
        """Extract JSON from response text, handling markdown code blocks and loose formatting."""
        if not text:
            return None
            
        # Clean up the text
        json_str = text.strip()
        
        # 1. Try to find JSON in markdown code block
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', json_str)
        if json_match:
            json_str = json_match.group(1).strip()
        
        # 2. Try direct parsing
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # 3. Try finding anything between braces { ... }
            obj_match = re.search(r'(\{[\s\S]*\})', json_str)
            if obj_match:
                try:
                    return json.loads(obj_match.group(1))
                except json.JSONDecodeError as e:
                    print(f"❌ JSON Parsing Error: {e}")
                    print(f"RAW RESPONSE START:\n{text}\nRAW RESPONSE END")
            else:
                print("❌ No JSON object found in response")
                print(f"RAW RESPONSE START:\n{text}\nRAW RESPONSE END")
        
        return None
