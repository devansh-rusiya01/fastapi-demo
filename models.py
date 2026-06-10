from pydantic import BaseModel
from typing import Optional

class UserSignup(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: Optional[str] = None
    role: str = "user"

class UserLogin(BaseModel):
    email: str
    password: str
