import os
import json
import uuid
from datetime import datetime, timezone
from app.config import EXAMS_DIR

os.makedirs(EXAMS_DIR, exist_ok=True)
EXAM_FILE = os.path.join(EXAMS_DIR, "exams.json")

if not os.path.exists(EXAM_FILE):
    with open(EXAM_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def _read_exams():
    with open(EXAM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_exams(exams):
    with open(EXAM_FILE, "w", encoding="utf-8") as f:
        json.dump(exams, f, indent=2)

def create_exam(data: dict):
    exams = _read_exams()

    for exam in exams:
        if exam["exam_id"] == data["exam_id"]:
            return None

    new_exam = {
        "id": str(uuid.uuid4()),
        "exam_id": data["exam_id"],
        "title": data["title"],
        "subject": data.get("subject"),
        "description": data.get("description"),
        "total_marks": data["total_marks"],
        "uploaded_by": data["uploaded_by"],
        "scheme_id": None,
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    exams.append(new_exam)
    _write_exams(exams)
    return new_exam

def get_exam_by_exam_id(exam_id: str):
    exams = _read_exams()
    for exam in exams:
        if exam["exam_id"] == exam_id:
            return exam
    return None

def list_exams_by_user(user_id: str):
    exams = _read_exams()
    return [exam for exam in exams if exam["uploaded_by"] == user_id]

def attach_scheme_to_exam(exam_id: str, scheme_id: str):
    exams = _read_exams()
    updated = None

    for exam in exams:
        if exam["exam_id"] == exam_id:
            exam["scheme_id"] = scheme_id
            updated = exam
            break

    _write_exams(exams)
    return updated