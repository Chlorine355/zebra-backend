from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import secrets
from sqlalchemy.orm import Session
from users.models import User
from fastapi import BackgroundTasks
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from const import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, SMTP_FROM, SMTP_HOST, SMTP_PASS, SMTP_PORT, SMTP_USER, BASE_URL


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_verification_token(db: Session, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=24)
    
    db.query(User).filter(User.id == user_id).update({
        "verification_token": token,
        "token_expires": expires
    })
    db.commit()
    return token

async def send_verification_email(email: str, token: str, background_tasks: BackgroundTasks):
    link = f"{BASE_URL}/api/auth/verify?token={token}"
    html = f"<p>Нажмите для подтверждения: <a href='{link}'>{link}</a></p>"
    
    # В продакшене: Resend, SendGrid, AWS SES или Celery + RQ
    background_tasks.add_task(
        _send_email_async, 
        to_email=email, 
        subject="Подтвердите email", 
        html_content=html
    )

def _send_email_async(to_email: str, subject: str, html_content: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)