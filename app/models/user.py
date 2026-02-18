from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    business_name: str
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: str
    business_id: str
    is_active: bool = True
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    email: Optional[str] = None
    business_id: Optional[str] = None