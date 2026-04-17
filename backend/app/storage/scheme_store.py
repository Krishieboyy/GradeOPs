import os
import json

SCHEME_DIR = "marking_schemes"
os.makedirs(SCHEME_DIR, exist_ok=True)

def save_scheme(scheme_id: str, data: dict):
    path = os.path.join(SCHEME_DIR, f"{scheme_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_scheme(scheme_id: str):
    path = os.path.join(SCHEME_DIR, f"{scheme_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)