"""
Utility functions for LexAssist.
Handles multimodal document parsing (PDF text extraction and Image OCR/analysis).
"""

import os
import io
from PIL import Image
from pypdf import PdfReader
from llm.gemini_client import get_gemini_client, generate_text

def process_uploaded_file(uploaded_file) -> str:
    """
    Parses an uploaded file (PDF or Image) and returns extracted text.
    """
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_uploaded_pdf(uploaded_file)
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_uploaded_image(uploaded_file)
    else:
        return f"Unsupported file format: {uploaded_file.name}"

def extract_text_from_uploaded_pdf(uploaded_file) -> str:
    """Extracts raw text from uploaded PDF file buffer."""
    try:
        pdf_bytes = uploaded_file.read()
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)
        pages_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages_text.append(text)

        full_text = "\n".join(pages_text).strip()
        if not full_text:
            return "[PDF Extraction Warning: No selectable text found. PDF may be a scanned image.]"
        return full_text
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

def extract_text_from_uploaded_image(uploaded_file) -> str:
    """
    Extracts text from scanned image/document photo using Gemini Multimodal Vision API.
    """
    try:
        image_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(image_bytes))

        client = get_gemini_client()
        if not client:
            return (
                f"[IMAGE UPLOAD RECEIVED: {uploaded_file.name} ({image.size[0]}x{image.size[1]} px)]\n"
                "To process scanned images with multimodal OCR, please add your GEMINI_API_KEY to .env."
            )

        prompt = (
            "Extract all legibly written or printed text from this legal document image. "
            "Return only the extracted text facts, accurately transcribed without commentary."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image]
        )
        return response.text if response.text else "No legibly written text detected in image."
    except Exception as e:
        return f"Error processing image document: {str(e)}"

