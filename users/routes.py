from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user, get_db, get_all_users, set_user_notifications
from .schemas import User, UsersResponse, Notifications
from .models import User as UserModel

router = APIRouter()

@router.get("/current", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/all", response_model=UsersResponse)
def read_read_all(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    users = get_all_users(db, current_user)
    return {'total': len(users), 'users': users}

@router.post("/notifications", response_model=Notifications)
def set_notifications(data: Notifications, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    result = set_user_notifications(data.receives_notifications, db, current_user)
    return result