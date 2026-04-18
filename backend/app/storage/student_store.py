import os
import json
import uuid
from datetime import datetime, timezone
from app.config import STUDENTS_DIR

os.makedirs(STUDENTS_DIR, exist_ok=True)
STUDENT_FILE = os.path.join(STUDENTS_DIR, "students.json")

if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def _read_students():
    with open(STUDENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_students(students):
    with open(STUDENT_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2)

def create_student(data: dict):
    students = _read_students()

    for student in students:
        if student["student_id"] == data["student_id"]:
            return None

    new_student = {
        "id": str(uuid.uuid4()),
        "student_id": data["student_id"],
        "name": data["name"],
        "department": data.get("department"),
        "batch": data.get("batch"),
        "created_by": data["created_by"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    students.append(new_student)
    _write_students(students)
    return new_student

def get_student_by_student_id(student_id: str):
    students = _read_students()
    for student in students:
        if student["student_id"] == student_id:
            return student
    return None

def list_students_by_user(user_id: str):
    students = _read_students()
    return [student for student in students if student["created_by"] == user_id]