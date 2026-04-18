from app.storage.user_store import create_user, get_user_by_email
from app.utils.security import hash_password, verify_password, create_access_token

def register_instructor(name: str, email: str, password: str):
    user = create_user(name, email, hash_password(password))
    if not user:
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }

def login_instructor(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    return {
        "access_token": create_access_token({
            "sub": user["id"],
            "email": user["email"],
            "role": user["role"]
        }),
        "token_type": "bearer"
    }