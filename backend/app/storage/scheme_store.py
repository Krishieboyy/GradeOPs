import os
import json
import uuid
from datetime import datetime, timezone
from app.config import SCHEMES_DIR

os.makedirs(SCHEMES_DIR, exist_ok=True)
SCHEME_FILE = os.path.join(SCHEMES_DIR, "schemes.json")

if not os.path.exists(SCHEME_FILE):
    with open(SCHEME_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def _read_schemes():
    with open(SCHEME_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_schemes(schemes):
    with open(SCHEME_FILE, "w", encoding="utf-8") as f:
        json.dump(schemes, f, indent=2)

def create_scheme(exam_id: str, uploaded_by: str, scheme_data: dict):
    schemes = _read_schemes()

    new_scheme = {
        "id": str(uuid.uuid4()),
        "scheme_id": str(uuid.uuid4()),
        "exam_id": exam_id,
        "uploaded_by": uploaded_by,
        "exam_name": scheme_data["exam_name"],
        "total_marks": scheme_data["total_marks"],
        "questions": scheme_data["questions"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    schemes.append(new_scheme)
    _write_schemes(schemes)
    return new_scheme

def get_scheme_by_scheme_id(scheme_id: str):
    schemes = _read_schemes()
    for scheme in schemes:
        if scheme["scheme_id"] == scheme_id:
            return scheme
    return None

def get_scheme_by_exam_id(exam_id: str):
    schemes = _read_schemes()
    filtered = [scheme for scheme in schemes if scheme["exam_id"] == exam_id]
    if not filtered:
        return None
    return filtered[-1]