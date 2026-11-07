"""
Google Gemini API Client Module for LexAssist.
Uses the official google-genai SDK for grounded RAG synthesis and multimodal extraction.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def get_gemini_client():
    """Returns official Gemini client if GEMINI_API_KEY is present, else None."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "your_gemini_api_key_here":
        return None
    return genai.Client(api_key=api_key)

def generate_text(prompt: str, system_instruction: str = None, model: str = "gemini-2.5-flash") -> str:
    """
    Generates text using Google Gemini API.
    If GEMINI_API_KEY is missing, provides an explainable fallback response.
    """
    client = get_gemini_client()
    if not client:
        return (
            "[LEXASSIST MOCK RESPONSE - API KEY NOT CONFIGURED]\n\n"
            "To activate live Gemini generation, please add your valid GEMINI_API_KEY to the .env file.\n\n"
            f"Prompt received: {prompt[:200]}..."
        )

    config = types.GenerateContentConfig(
        temperature=0.2, # Low temperature for factual grounded legal reasoning
        top_p=0.9,
    )
    if system_instruction:
        config.system_instruction = system_instruction

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config
        )
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {str(e)}"

if __name__ == "__main__":
    client_status = "Available" if get_gemini_client() else "Not configured in .env"
    print(f"Gemini Client Status: {client_status}")

