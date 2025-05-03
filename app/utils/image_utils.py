from PIL import Image
import pytesseract
from typing import BinaryIO
import io

async def extract_text_from_image(file: BinaryIO) -> str:
    """
    Extrait le texte d'une image en utilisant Tesseract OCR.
    """
    try:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        text = pytesseract.image_to_string(image, lang='fra')
        return text.strip()
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction du texte depuis l'image: {str(e)}")
