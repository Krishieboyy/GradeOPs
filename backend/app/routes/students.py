from fastapi import APIRouter, Depends, HTTPException
from app.schemas.student_schema import StudentCreateRequest, StudentResponse
from app.services.student_service import create_student_record, get_student_record, list_student_records
from app.utils.auth_guard import get_current_instructor

router = APIRouter()

@router.post("/create", response_model=StudentResponse)
def create_student(req: StudentCreateRequest, current_user: dict = Depends(get_current_instructor)):
    data = req.model_dump()
    data["created_by"] = current_user["id"]

    created = create_student_record(data)
    if not created:
        raise HTTPException(status_code=400, detail="Student ID already exists")

    return created

@router.get("/", response_model=list[StudentResponse])
def list_students(current_user: dict = Depends(get_current_instructor)):
    return list_student_records(current_user["id"])

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, current_user: dict = Depends(get_current_instructor)):
    student = get_student_record(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student