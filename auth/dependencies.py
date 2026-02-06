import aiofiles
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from const import ALGORITHM, SECRET_KEY
from reports.schemas import ReportCreate
from .utils import verify_password, get_password_hash, create_access_token
from .models import TokenData
from users.models import User
from reports.models import Report
from assets.models import Asset
from .database import SessionLocal, engine, Base
import datetime

Base.metadata.create_all(bind=engine)


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
    if current_user.is_admin:
        report = db.query(Report).filter(Report.id == report_id).first() # admin can access any report
    else:
        report = db.query(Report).filter(Report.id == report_id, Report.user_id == current_user.id ).first() # users can access only their reports
    if report is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Report {report_id} does not exist",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return report


def get_reports(db: Session, user: User):
    if user.is_admin:
        reports = db.query(Report).all() # get all
    else:
        reports = db.query(Report).filter(Report.user_id == user.id).all() # get user's
    if reports is None: 
        return []
    return reports
async def create_report(db: Session, report: ReportCreate, current_user: User):
    now = datetime.datetime.now()
    db_report = Report(violation=report.violation, 
                    user_id=current_user.id, 
                    datetime=datetime.datetime.fromisoformat(report.datetime), 
                    lat=report.lat, 
                    lon=report.lon, 
                    description=report.description, 
                    status='pending',
                    report_datetime=now,
                    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    for asset in report.assets:
        path = 'upload/' + asset.filename
        async with aiofiles.open(path, 'wb') as out_file:
            content = await asset.read()
            await out_file.write(content)
            db_asset = Asset(user_id=current_user.id,report_id=db_report.id, datetime=now, uri=path)
            db.add(db_asset) 
   
    db.commit()
    return db_report