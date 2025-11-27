from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=72)
    email: EmailStr

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password cannot exceed 72 bytes')
        return v

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=72)

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password cannot exceed 72 bytes')
        return v

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    message: str
    username: str
    email: str
    id: int            # ✅ must be here
    user_id: int
    access_token: str

class UserProfileUpdate(BaseModel):
    """Schema for updating user profile (username and/or email)"""
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v

class PasswordChange(BaseModel):
    """Schema for changing user password"""
    old_password: str = Field(..., min_length=8, max_length=72)
    new_password: str = Field(..., min_length=8, max_length=72)

    @field_validator('old_password', 'new_password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password cannot exceed 72 bytes')
        return v

    @field_validator('new_password')
    @classmethod
    def validate_new_password_different(cls, v, info):
        if 'old_password' in info.data and v == info.data['old_password']:
            raise ValueError('New password must be different from old password')
        return v
