import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from app.config import UPLOAD_DIR
from app.schemas.evaluation_schema import SchemeUploadResponse, EvaluationResponse
from app.services.marking_scheme_service import upload_marking_scheme
from app.services.evaluation_service import evaluate_answer_text
from app.services.ocr_service import extract_text_from_image
from app.services.submission_service import create_submission_record, create_evaluation_record
from app.storage.scheme_store import get_scheme_by_exam_id
from app.storage.student_store import get_student_by_student_id
from app.utils.image_loader import load_image
from app.utils.auth_guard import get_current_instructor

router = APIRouter()
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-scheme", response_model=SchemeUploadResponse)
async def upload_scheme(
    exam_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_instructor)
):
    content = await file.read()
    result, err = upload_marking_scheme(exam_id, current_user["id"], content)

    if err:
        raise HTTPException(status_code=404, detail=err)

    return result

@router.post("/grade", response_model=EvaluationResponse)
async def grade_answer_sheet(
    exam_id: str = Form(...),
    student_id: str = Form(...),
    answer_sheet: UploadFile = File(...),
    current_user: dict = Depends(get_current_instructor)
):
    scheme = get_scheme_by_exam_id(exam_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="No marking scheme found for this exam")

    student = get_student_by_student_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    filename = f"{student_id}_{exam_id}_{answer_sheet.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await answer_sheet.read())

    image = load_image(file_path)
    extracted_text = extract_text_from_image(image)

    submission = create_submission_record({
        "exam_id": exam_id,
        "scheme_id": scheme["scheme_id"],
        "student_id": student_id,
        "uploaded_by": current_user["id"],
        "image_path": file_path,
        "extracted_text": extracted_text,
        "status": "evaluated"
    })

    result = evaluate_answer_text(extracted_text, scheme)

    evaluation = create_evaluation_record({
        "submission_id": submission["id"],
        "scheme_id": scheme["scheme_id"],
        "exam_id": exam_id,
        "student_id": student_id,
        "evaluated_by": current_user["id"],
        "extracted_text": result["extracted_text"],
        "total_score": result["total_score"],
        "max_score": result["max_score"],
        "percentage": result["percentage"],
        "question_wise": result["question_wise"],
        "overall_reasoning": result["overall_reasoning"]
    })

    return {
        "evaluation_id": evaluation["id"],
        "submission_id": submission["id"],
        "scheme_id": scheme["scheme_id"],
        "exam_id": exam_id,
        "student_id": student_id,
        "extracted_text": result["extracted_text"],
        "total_score": result["total_score"],
        "max_score": result["max_score"],
        "percentage": result["percentage"],
        "question_wise": result["question_wise"],
        "overall_reasoning": result["overall_reasoning"],
        "created_at": evaluation["created_at"]
    }