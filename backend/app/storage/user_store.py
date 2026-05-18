import os
import json
import uuid
from datetime import datetime, timezone
from app.config import DATA_DIR

USERS_DIR = os.path.join(DATA_DIR, "users")
USER_FILE = os.path.join(USERS_DIR, "users.json")

os.makedirs(USERS_DIR, exist_ok=True)

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def _read_users():
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def create_user(name: str, email: str, hashed_password: str):
    users = _read_users()

    for user in users:
        if user["email"].lower() == email.lower():
            return None

    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email.lower(),
        "hashed_password": hashed_password,
        "role": "instructor",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    users.append(new_user)
    _write_users(users)
    return new_user

def get_user_by_email(email: str):
    users = _read_users()

    for user in users:
        if user["email"].lower() == email.lower():
            return user

    return None

def get_user_by_id(user_id: str):
    users = _read_users()

    for user in users:
        if user["id"] == user_id:
            return user

    return None