"""
User Pydantic models for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class UserRegister(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: str
    created_at: datetime
    resume_uploaded: bool = False
    total_interviews: int = 0
    avg_score: float = 0.0

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ResumeData(BaseModel):
    """Parsed resume data"""
    skills: List[str] = []
    projects: List[str] = []
    experience: List[str] = []
    raw_text: str = ""
