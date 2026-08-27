from fastapi import FastAPI, UploadFile, File
from app.processing.ocr import extract_text_from_pdf

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/extract")
async def extract_form(file: UploadFile = File(...)):
    contents = await file.read()

    pages = extract_text_from_pdf(contents)

    return {
        "filename": file.filename,
        "page": pages
    }