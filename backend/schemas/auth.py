from pydantic import BaseModel
from typing import Optional
from backend.core.enums import UserRole

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserQuickLoginRequest(BaseModel):
    role: UserRole

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: int

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
