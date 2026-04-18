from app.storage.exam_store import create_exam, get_exam_by_exam_id, list_exams_by_user

def create_exam_record(data: dict):
    return create_exam(data)

def get_exam_record(exam_id: str):
    return get_exam_by_exam_id(exam_id)

def list_exam_records(user_id: str):
    return list_exams_by_user(user_id)