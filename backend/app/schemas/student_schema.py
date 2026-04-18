from pydantic import BaseModel
from typing import Optional

class StudentCreateRequest(BaseModel):
    student_id: str
    name: str
    department: Optional[str] = None
    batch: Optional[str] = None

class StudentResponse(BaseModel):
    id: str
    student_id: str
    name: str
    department: Optional[str] = None
    batch: Optional[str] = None
    created_by: str
    created_at: str