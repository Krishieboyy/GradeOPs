import json
import uuid
from app.schemas.evaluation_schema import MarkingScheme
from app.storage.scheme_store import save_scheme

def upload_marking_scheme(file_bytes: bytes) -> dict:
    data = json.loads(file_bytes.decode("utf-8"))
    scheme = MarkingScheme(**data)

    scheme_id = str(uuid.uuid4())
    save_scheme(scheme_id, scheme.model_dump())

    return {
        "scheme_id": scheme_id,
        "exam_name": scheme.exam_name,
        "total_marks": scheme.total_marks,
        "question_count": len(scheme.questions)
    }