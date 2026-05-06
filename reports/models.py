from sqlalchemy import Column, Integer, String, DateTime, Float
from auth.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True)
    
    violation = Column(String)
    datetime = Column(DateTime)
    lat = Column(Float)
    lon = Column(Float)
    description = Column(String)
    
    report_datetime = Column(DateTime)
    status = Column(String)
    address = Column(String, nullable=True)
    gosnomer = Column(String, nullable=True)
