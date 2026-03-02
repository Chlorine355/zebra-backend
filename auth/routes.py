import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .dependencies import get_db, authenticate_user, get_user
from .utils import create_access_token, generate_verification_token, send_verification_email 
from .models import Token
from .schemas import UserCreate, UserResponse
from users.models import User
from .utils import get_password_hash

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm requiers username. Use email ever after
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db), background_tasks = BackgroundTasks):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already registered")
    hashed_password = get_password_hash(user.password)
    now = datetime.datetime.now()

    db_user = User(email=user.email, hashed_password=hashed_password, created_at=now, updated_at=now, last_login=now)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if db_user.id == 1: # the first user is assigned admin
        db.query(User).filter(User.id == db_user.id).update({'is_admin': True})
        db.commit()
    verification_token = generate_verification_token(db, db_user.id) # TODO: 1 query, use user
    send_verification_email(db_user.email, verification_token, background_tasks)
    return db_user

@router.get("/verify", status_code=200)
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(400, "Недействительный или уже использованный токен")
        
    if user.token_expires <  datetime.datetime.now(datetime.timezone.utc):
        raise HTTPException(400, "Срок действия токена истёк")
        
    user.is_verified = True
    user.verification_token = None
    user.token_expires = None
    db.commit()
    
    return {"message": "Email успешно подтверждён"}