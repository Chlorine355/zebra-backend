from pydantic import BaseModel

class ReportShort(BaseModel):
    username: str

class ReportCreate(ReportShort):
    password: str

class ReportFull(ReportShort):
    id: int
    is_active: bool
    receives_notifications: bool

    class Config:
        orm_mode = True
