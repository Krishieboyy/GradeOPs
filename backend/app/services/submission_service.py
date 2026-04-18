from app.storage.submission_store import create_submission
from app.storage.evaluation_store import create_evaluation

def create_submission_record(data: dict):
    return create_submission(data)

def create_evaluation_record(data: dict):
    return create_evaluation(data)