from pydantic import BaseModel

class SubmissionResponse(BaseModel):
    id: str
    exam_id: str
    scheme_id: str
    student_id: str
    uploaded_by: str
    image_path: str
    extracted_text: str
    status: str
    created_at: str