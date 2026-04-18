from fastapi import APIRouter, Depends
from app.storage.submission_store import list_submissions_by_exam, list_submissions_by_student
from app.storage.evaluation_store import list_evaluations_by_exam, list_evaluations_by_student
from app.utils.auth_guard import get_current_instructor

router = APIRouter()

@router.get("/exam/{exam_id}")
def get_exam_submissions(exam_id: str, current_user: dict = Depends(get_current_instructor)):
    return {
        "submissions": list_submissions_by_exam(exam_id),
        "evaluations": list_evaluations_by_exam(exam_id)
    }

@router.get("/student/{student_id}")
def get_student_submissions(student_id: str, current_user: dict = Depends(get_current_instructor)):
    return {
        "submissions": list_submissions_by_student(student_id),
        "evaluations": list_evaluations_by_student(student_id)
    }