from fastapi import FastAPI, UploadFile, File
from app.ocr_engine import OCREngine
import shutil

app = FastAPI()
ocr = OCREngine()

@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    with open(f"temp_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ocr.recognize_text(f"temp_{file.filename}")
    return {"result": result}
