from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.controllers import user_controller
from src.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api", tags=["Users"])
bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, user.model_dump())

@router.post("/users/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return user_controller.authenticate_user(db, user.email, user.password)

@router.get("/user", response_model=UserResponse)
def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # здесь уже чистый токен
    return user_controller.get_current_user(db, token)

@router.put("/user", response_model=UserResponse)
def update_user_route(
    user: UserCreate,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    current = user_controller.get_current_user(db, token)
    return user_controller.update_user(db, current.id, user.model_dump())
