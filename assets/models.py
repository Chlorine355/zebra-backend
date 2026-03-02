from sqlalchemy import Boolean, Column, Integer, String, DateTime
from auth.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    created_at = Column(DateTime)
    s3_key = Column(String)
    filename = Column(String)
    is_video = Column(Boolean, default=False)
    file_hash = Column(String(64))
    
