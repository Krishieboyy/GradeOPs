from pydantic import BaseModel
from typing import Optional

class ExamCreateRequest(BaseModel):
    exam_id: str
    title: str
    subject: Optional[str] = None
    description: Optional[str] = None
    total_marks: float

class ExamResponse(BaseModel):
    id: str
    exam_id: str
    title: str
    subject: Optional[str] = None
    description: Optional[str] = None
    total_marks: float
    uploaded_by: str
    scheme_id: Optional[str] = None
    is_active: bool
    created_at: str