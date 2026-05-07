from sqlalchemy import Boolean, Column, Integer, String
from auth.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    daily_reports = Column(Integer, default=0)
    receives_notifications = Column(Boolean, default=False) 