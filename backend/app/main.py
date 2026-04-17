from fastapi import FastAPI
from app.routes.ocr import router as ocr_router
from app.routes.evaluate import router as evaluate_router

app = FastAPI(title="OCR Evaluation Backend")

app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
app.include_router(evaluate_router, prefix="/evaluate", tags=["Evaluation"])

@app.get("/")
def root():
    return {"message": "OCR Evaluation Backend is running"}