from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/extract")
async def extract_form(file: UploadFile = File(...)):
    contents = await file.read()

    return {
        "filename": file.filename,
        "size": len(contents)
    }