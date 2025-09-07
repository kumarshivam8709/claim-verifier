import requests
import trafilatura
from PIL import Image
import pytesseract
import os

def fetch_url_content(url: str) -> str:
    """Fetches text content from a given URL."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded, favor_recall=True)
        return "Could not fetch content."
    except Exception as e:
        return f"Error fetching URL: {e}"

def extract_text_from_image(image_bytes: bytes) -> str:
    """Uses OCR.space API to extract text from an image."""
    api_key = os.environ.get("OCR_SPACE_API_KEY")
    if not api_key:
        return "OCR_SPACE_API_KEY not set in .env"

    try:
        response = requests.post(
            'https://api.ocr.space/parse/image',
            headers={'apikey': api_key},
            files={'filename': ('image.png', image_bytes, 'image/png')},
            data={'language': 'eng', 'isOverlayRequired': False}
        )
        data = response.json()
        if data.get("IsErroredOnProcessing"):
            return f"OCR Error: {data.get('ErrorMessage')}"
        
        parsed_text = data.get("ParsedResults", [{}])[0].get("ParsedText", "")
        return parsed_text
    except Exception as e:
        return f"Error with OCR API: {e}"