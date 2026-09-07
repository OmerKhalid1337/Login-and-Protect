from pydantic import BaseModel, EmailStr
from typing import Optional, Any, Dict

class AuthCredentials(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: Optional[str] = None
    created_at: Optional[str] = None
    app_metadata: Optional[Dict[str, Any]] = None
    user_metadata: Optional[Dict[str, Any]] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    user: Optional[UserResponse] = None
