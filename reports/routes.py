from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user, get_db
from .schemas import ReportShort, ReportFull
from .models import Report as ReportModel
from ..users.models import User as UserModel

router = APIRouter()

@router.get("/all_user_reports", response_model=ReportShort)
def read_user_reports(current_user: UserModel = Depends(get_current_user)):
    # get reports of current user and return them
    return current_user


@router.get("/user_report_by_id", response_model=ReportFull)
def read_user_reports(report_id: int, current_user: UserModel = Depends(get_current_user)):
    # get report of current user by id and return it
    return current_user