from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user, get_db, get_all_users
from .schemas import User, UsersResponse
from .models import User as UserModel

router = APIRouter()

@router.get("/current", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    print(current_user)
    return current_user

@router.get("/all", response_model=UsersResponse)
def read_read_all(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    users = get_all_users(db, current_user)
    return {'total': len(users), 'users': users}