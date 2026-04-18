from app.storage.student_store import create_student, get_student_by_student_id, list_students_by_user

def create_student_record(data: dict):
    return create_student(data)

def get_student_record(student_id: str):
    return get_student_by_student_id(student_id)

def list_student_records(user_id: str):
    return list_students_by_user(user_id)