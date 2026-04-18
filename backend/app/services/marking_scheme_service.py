import json
from app.schemas.evaluation_schema import MarkingScheme
from app.storage.scheme_store import create_scheme
from app.storage.exam_store import get_exam_by_exam_id, attach_scheme_to_exam

def upload_marking_scheme(exam_id: str, uploaded_by: str, file_bytes: bytes):
    exam = get_exam_by_exam_id(exam_id)
    if not exam:
        return None, "Exam not found"

    data = json.loads(file_bytes.decode("utf-8"))
    scheme = MarkingScheme(**data)

    created = create_scheme(exam_id, uploaded_by, scheme.model_dump())
    attach_scheme_to_exam(exam_id, created["scheme_id"])

    return {
        "scheme_id": created["scheme_id"],
        "exam_id": exam_id,
        "exam_name": created["exam_name"],
        "total_marks": created["total_marks"],
        "question_count": len(created["questions"])
    }, None