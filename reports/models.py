from sqlalchemy import Boolean, Column, Integer, String, DateTime
from auth.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, index=True)
    
    violation = Column(String)
    datetinme = Column(DateTime)
    lat = Column(String)
    lon = Column(String)
    description = Column(String)
    
    report_datetime = datetinme = Column(DateTime)
    status = Column(String)
    address = Column(String, nullable=True)
    gosnomer = Column(String, nullable=True)
