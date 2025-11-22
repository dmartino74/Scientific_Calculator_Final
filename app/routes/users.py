from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.operations.schemas.user_schemas import (
    UserCreate, UserLogin, UserRead, LoginResponse
)
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=LoginResponse, status_code=200)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # enforce password length constraints
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="Password must not exceed 72 characters")

    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.username, "user_id": new_user.id})

    return {
        "message": "Registration successful",
        "username": new_user.username,
        "email": new_user.email,
        "id": new_user.id,
        "user_id": new_user.id,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=LoginResponse, status_code=200)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username, "user_id": db_user.id})

    return {
        "message": "Login successful",
        "username": db_user.username,
        "email": db_user.email,
        "id": db_user.id,
        "user_id": db_user.id,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserRead)
def get_current_user(db: Session = Depends(get_db)):
    # placeholder until authentication is wired in
    raise HTTPException(status_code=501, detail="Not implemented - requires authentication")
