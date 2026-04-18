import os

MODEL_NAME = os.getenv("MODEL_NAME", "JackChew/Qwen2-VL-2B-OCR")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 2048))

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

DATA_DIR = os.getenv("DATA_DIR", "data")
USERS_DIR = os.path.join(DATA_DIR, "users")
EXAMS_DIR = os.path.join(DATA_DIR, "exams")
STUDENTS_DIR = os.path.join(DATA_DIR, "students")
SCHEMES_DIR = os.path.join(DATA_DIR, "schemes")
SUBMISSIONS_DIR = os.path.join(DATA_DIR, "submissions")
EVALUATIONS_DIR = os.path.join(DATA_DIR, "evaluations")