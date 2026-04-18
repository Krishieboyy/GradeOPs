from fastapi import APIRouter, Depends, HTTPException
from app.schemas.exam_schema import ExamCreateRequest, ExamResponse
from app.services.exam_service import create_exam_record, get_exam_record, list_exam_records
from app.utils.auth_guard import get_current_instructor

router = APIRouter()

@router.post("/create", response_model=ExamResponse)
def create_exam(req: ExamCreateRequest, current_user: dict = Depends(get_current_instructor)):
    data = req.model_dump()
    data["uploaded_by"] = current_user["id"]

    created = create_exam_record(data)
    if not created:
        raise HTTPException(status_code=400, detail="Exam ID already exists")

    return created

@router.get("/", response_model=list[ExamResponse])
def list_exams(current_user: dict = Depends(get_current_instructor)):
    return list_exam_records(current_user["id"])

@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(exam_id: str, current_user: dict = Depends(get_current_instructor)):
    exam = get_exam_record(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam