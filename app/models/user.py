from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db import get_db
from app.models.user import User
from app.operations.schemas.user_schemas import UserCreate, UserLogin, UserRead

router = APIRouter(tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # bcrypt only supports up to 72 bytes
    encoded = password.encode("utf-8")
    if len(encoded) > 72:
        # truncate safely instead of raising
        encoded = encoded[:72]
    return pwd_context.hash(encoded.decode("utf-8", errors="ignore"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    encoded = plain_password.encode("utf-8")
    if len(encoded) > 72:
        encoded = encoded[:72]
    return pwd_context.verify(encoded.decode("utf-8", errors="ignore"), hashed_password)

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "user_id": db_user.id}

