from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel
from datetime import datetime as datetime_type

from assets.schemas import Asset


class ReportShort(BaseModel):
    id: int
    violation: str
    datetime: datetime_type
    status: str

class ReportsShortResponse(BaseModel):
    reports: List[ReportShort]
    

class ReportFull(ReportShort):
    user_id: int
    lat: float
    lon: float
    description: str
    report_datetime: datetime_type
    address: str | None
    gosnomer: str | None
    assets: List[Asset] # TODO: figure out the best way

    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    violation: str
    datetime: str
    lat: float
    lon: float
    description: str
    assets: List[UploadFile] | None


class ReportCreateResponse(BaseModel):
    report_id: int