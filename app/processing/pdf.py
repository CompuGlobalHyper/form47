import pymupdf
import pytesseract
from PIL import Image
from io import BytesIO

def extract_pdf(contents: bytes):
    document = pymupdf.open(
        stream=contents,
        filetype="pdf"
    )

    fields = extract_form_fields(document)
    pages = []


    for page in document:
        text = page.get_text().strip()

        if text:
            pages.append({
                "method": "text",
                "text": text
            })
        else:
            text = extract_with_ocr(page)
            pages.append({
                "method": "ocr",
                "text": text
            })

    return {
        "fields": fields,
        "pages": pages
    }


def extract_form_fields(document):

    fields = {}

    for page in document:
        widgets = page.widgets()

        if widgets is None:
            continue

        for widget in widgets:
            if widget.field_value is not None:
                fields[widget.field_name] = widget.field_value
    return fields

def extract_with_ocr(page):
    pixmap = page.get_pixmap(dpi=400)
    
    image = Image.open(
        BytesIO(pixmap.tobytes("png"))
    )

    rawData = pytesseract.image_to_data(
        image,
        config="--psm 6",
        output_type=pytesseract.Output.DICT
    )

    data = []

    for i, text in enumerate(rawData["text"]):
        if text.strip():
            data.append({
                "text": text,
                "x": rawData["left"][i],
                "y": rawData["top"][i],
                "width": rawData["width"][i],
                "height": rawData["height"][i],
                "confidence": rawData["conf"][i]
            })

    return data
