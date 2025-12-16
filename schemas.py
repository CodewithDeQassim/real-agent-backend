"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# User Role Type
UserRole = Literal['Admin', 'Player', 'Agent', 'Club Manager']

class UserBase(BaseModel):
    """Base schema with common user fields"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=6, max_length=50)

class UserUpdate(BaseModel):
    """Schema for updating user - all fields optional"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=6, max_length=50)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """Schema for user response (without password)"""
    user_id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True  # Allows compatibility with SQLAlchemy models

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """Schema for login response"""
    success: bool
    message: str
    user: Optional[UserResponse] = None

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True