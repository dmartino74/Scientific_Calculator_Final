from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.operations.schemas.user_schemas import (
    UserCreate, UserLogin, UserRead, LoginResponse, UserProfileUpdate, PasswordChange
)
from app.security import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)) -> User:
    """Dependency to get the currently authenticated user from the Authorization header."""
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("user_id") or payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    # If user_id is username (string), try to find by username
    if isinstance(user_id, str):
        user = db.query(User).filter(User.username == user_id).first()
    else:
        user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

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
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's profile"""
    return current_user


@router.put("/me", response_model=UserRead)
def update_user_profile(profile: UserProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update current user's profile (username and/or email)"""
    # Check if username is being changed and if it already exists
    if profile.username and profile.username != current_user.username:
        existing_user = db.query(User).filter(User.username == profile.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        current_user.username = profile.username
    
    # Check if email is being changed and if it already exists
    if profile.email and profile.email != current_user.email:
        existing_email = db.query(User).filter(User.email == profile.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = profile.email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.post("/me/change-password")
def change_password(password_data: PasswordChange, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Change current user's password"""
    # Verify old password
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    
    # Hash and save new password
    current_user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}
