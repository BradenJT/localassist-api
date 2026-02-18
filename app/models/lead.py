from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
from uuid import uuid4

class LeadBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+?1?\d{10,15}$')
    company: Optional[str] = Field(None, max_length=200)
    message: Optional[str] = Field(None, max_length=2000)
    source: Literal["website", "referral", "social", "other"] = "website"
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        # Strip all non-digits
        digits = ''.join(filter(str.isdigit, v))
        if len(digits) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return digits

class LeadCreate(LeadBase):
    # business_id is NOT required from the user - it's set by the API
    pass

class Lead(LeadBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    business_id: str
    status: Literal["new", "contacted", "qualified", "converted", "lost"] = "new"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }

class LeadUpdate(BaseModel):
    status: Optional[Literal["new", "contacted", "qualified", "converted", "lost"]] = None
    message: Optional[str] = None

class LeadResponse(Lead):
    pass