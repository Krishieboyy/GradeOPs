import uuid
from datetime import datetime, timezone
from app.db.mongo import users_collection

def create_user(name: str, email: str, hashed_password: str):

    existing = users_collection.find_one({
        "email": email.lower()
    })

    if existing:
        return None

    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email.lower(),
        "hashed_password": hashed_password,
        "role": "instructor",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    users_collection.insert_one(new_user)

    return new_user

def get_user_by_email(email: str):

    return users_collection.find_one({
        "email": email.lower()
    })

def get_user_by_id(user_id: str):

    return users_collection.find_one({
        "id": user_id
    })