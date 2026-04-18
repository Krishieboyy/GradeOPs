import os
import json
import uuid
from datetime import datetime, timezone
from app.config import EVALUATIONS_DIR

os.makedirs(EVALUATIONS_DIR, exist_ok=True)
EVALUATION_FILE = os.path.join(EVALUATIONS_DIR, "evaluations.json")

if not os.path.exists(EVALUATION_FILE):
    with open(EVALUATION_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def _read_evaluations():
    with open(EVALUATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_evaluations(evaluations):
    with open(EVALUATION_FILE, "w", encoding="utf-8") as f:
        json.dump(evaluations, f, indent=2)

def create_evaluation(data: dict):
    evaluations = _read_evaluations()

    new_eval = {
        "id": str(uuid.uuid4()),
        "submission_id": data["submission_id"],
        "scheme_id": data["scheme_id"],
        "exam_id": data["exam_id"],
        "student_id": data["student_id"],
        "evaluated_by": data["evaluated_by"],
        "extracted_text": data["extracted_text"],
        "total_score": data["total_score"],
        "max_score": data["max_score"],
        "percentage": data["percentage"],
        "question_wise": data["question_wise"],
        "overall_reasoning": data["overall_reasoning"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    evaluations.append(new_eval)
    _write_evaluations(evaluations)
    return new_eval

def list_evaluations_by_exam(exam_id: str):
    evaluations = _read_evaluations()
    return [e for e in evaluations if e["exam_id"] == exam_id]

def list_evaluations_by_student(student_id: str):
    evaluations = _read_evaluations()
    return [e for e in evaluations if e["student_id"] == student_id]