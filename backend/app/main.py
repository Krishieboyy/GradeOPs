from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.ocr import router as ocr_router
from app.routes.evaluate import router as evaluate_router
from app.routes.exams import router as exams_router
from app.routes.students import router as students_router
from app.routes.submissions import router as submissions_router

app = FastAPI(title="GradeOps Backend")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(exams_router, prefix="/exams", tags=["Exams"])
app.include_router(students_router, prefix="/students", tags=["Students"])
app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
app.include_router(evaluate_router, prefix="/evaluate", tags=["Evaluation"])
app.include_router(submissions_router, prefix="/submissions", tags=["Submissions"])

@app.get("/")
def root():
    return {"message": "GradeOps Backend is running"}