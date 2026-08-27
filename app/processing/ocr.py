import pymupdf
import pytesseract
from PIL import Image
from io import BytesIO

def extract_text_from_pdf(contents: bytes):
    document = pymupdf.open(
        stream=contents,
        filetype="pdf"
    )

    pages = []

    for page in document:
        pixmap = page.get_pixmap(dpi=300)

        image = Image.open(
            BytesIO(pixmap.tobytes("png"))
        )

        text = pytesseract.image_to_string(image)

        pages.append(text)
    return
    