from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    daily_reports: int
    receives_notifications: bool

    class Config:
        from_attributes = True
        
class UsersResponse(BaseModel):
    total: int
    users: List[User]

class Notifications(BaseModel):
    receives_notifications: bool