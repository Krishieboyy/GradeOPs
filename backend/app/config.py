import os

MODEL_NAME = os.getenv("MODEL_NAME", "JackChew/Qwen2-VL-2B-OCR")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 2048))