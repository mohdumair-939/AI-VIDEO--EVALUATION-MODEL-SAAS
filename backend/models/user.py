from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    email: str
    password: str
    role: str  # "student" | "mentor" | "admin"
    name: Optional[str] = None