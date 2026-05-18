import aiofiles
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

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

def get_all_users(db: Session, current_user: User):
    if not current_user.is_admin:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You can't access this endpoint",
    )
    users = db.query(User).all()
    return users


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
    assets = db.query(Asset).filter(Asset.report_id == report.id).all()
    report.assets = assets
    return report


def get_reports(db: Session, user: User):
    if user.is_admin:
        reports = db.query(Report).order_by(desc(Report.id)).all() # get all
    else:
        reports = db.query(Report).filter(Report.user_id == user.id).order_by(desc(Report.id)).all() # get user's
    if reports is None: 
        return []
    return reports

def get_reports_geo(db: Session, user: User):
    if user.is_admin:
        reports = db.query(Report.lat, Report.lon).all() # get all
    else:
        return []
    if reports is None: 
        return []
    return reports

async def create_report(db: Session, report: ReportCreate, current_user: User):
    now = datetime.datetime.now()
    # create report and get its id
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
    # save assets
    for asset in report.assets:
        path = 'upload/' + asset.filename
        async with aiofiles.open(path, 'wb', encoding='utf-8') as out_file:
            content = await asset.file.read()
            await out_file.write(content)
            db_asset = Asset(user_id=current_user.id,report_id=db_report.id, datetime=now, uri=path)
            db.add(db_asset) 
    # increment user's daily_reports
    db.query(User).filter(User.id == current_user.id).update({User.daily_reports: User.daily_reports + 1})
    db.commit()
    return db_report

def get_stats(db: Session, user: User):
    stats = db.query(Report.status, func.count(Report.status)).filter(Report.user_id == user.id).group_by(Report.status).all()
    return stats

def set_user_notifications(value, db: Session, current_user: User):
    db.query(User).filter(User.id == current_user.id).update({User.receives_notifications: value})
    db.commit()
    return {'receives_notifications': value}