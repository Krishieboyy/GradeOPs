from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import register_instructor, login_instructor

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(req: RegisterRequest):
    user = register_instructor(req.name, req.email, req.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    token = login_instructor(req.email, req.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return token