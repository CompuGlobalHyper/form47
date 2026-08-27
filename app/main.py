from fastapi import FastAPI, UploadFile, File
from app.processing.pdf import extract_pdf

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/extract")
async def extract_form(file: UploadFile = File(...)):
    contents = await file.read()

    result = extract_pdf(contents)

    return {
        "filename": file.filename,
        "result": result
    }