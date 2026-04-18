import os
import json
import uuid
from datetime import datetime, timezone
from app.config import SUBMISSIONS_DIR

os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
SUBMISSION_FILE = os.path.join(SUBMISSIONS_DIR, "submissions.json")

if not os.path.exists(SUBMISSION_FILE):
    with open(SUBMISSION_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def _read_submissions():
    with open(SUBMISSION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_submissions(submissions):
    with open(SUBMISSION_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=2)

def create_submission(data: dict):
    submissions = _read_submissions()

    new_submission = {
        "id": str(uuid.uuid4()),
        "exam_id": data["exam_id"],
        "scheme_id": data["scheme_id"],
        "student_id": data["student_id"],
        "uploaded_by": data["uploaded_by"],
        "image_path": data["image_path"],
        "extracted_text": data["extracted_text"],
        "status": data.get("status", "evaluated"),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    submissions.append(new_submission)
    _write_submissions(submissions)
    return new_submission

def get_submission_by_id(submission_id: str):
    submissions = _read_submissions()
    for submission in submissions:
        if submission["id"] == submission_id:
            return submission
    return None

def list_submissions_by_exam(exam_id: str):
    submissions = _read_submissions()
    return [s for s in submissions if s["exam_id"] == exam_id]

def list_submissions_by_student(student_id: str):
    submissions = _read_submissions()
    return [s for s in submissions if s["student_id"] == student_id]