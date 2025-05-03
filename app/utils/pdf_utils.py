import pdfplumber
from typing import BinaryIO

def extract_text_from_pdf(file: BinaryIO) -> str:
    file.seek(0)
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text