from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from reports.schemas import ReportCreate
from .utils import verify_password, get_password_hash, create_access_token
from .models import TokenData
from users.models import User
from reports.models import Report
from .database import SessionLocal, engine, Base
import datetime

Base.metadata.create_all(bind=engine)
# TODO: actual values
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_report(db: Session, current_user: User, report_id: int):
    report = db.query(Report).filter(Report.id == report_id, Report.user_id == current_user.id).first()
    if report is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Report {report_id} does not exist",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return report


def get_reports(db: Session, user_id: int):
    reports = db.query(Report).filter(Report.user_id == user_id).all()
    if reports is None: 
        return []
    return reports

def create_report(db: Session, report: ReportCreate, current_user: User):
    report = Report(violation=report.violation, 
                    user_id=current_user.id, 
                    datetime=datetime.datetime.fromisoformat(report.datetime), 
                    lat=report.lat, 
                    lon=report.lon, 
                    description=report.description, 
                    status='pending',
                    report_datetime=datetime.datetime.now(),
                    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report