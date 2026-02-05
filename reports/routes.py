from fastapi import APIRouter, Depends
from auth.dependencies import create_report, get_current_user, get_db, get_report, get_reports
from .schemas import ReportCreate, ReportCreateResponse, ReportFull, ReportsShortResponse
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/all", response_model=ReportsShortResponse)
def reports_all(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    reports = get_reports(db, user_id=current_user.id)
    return {'reports': reports}


@router.get("/one_by_id", response_model=ReportFull)
def report_one_by_id(report_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    report = get_report(db, current_user, report_id=report_id)
    return report

@router.post("/create", response_model=ReportCreateResponse)
def reports_create(report: ReportCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    report = create_report(db, report, current_user)
    return {'report_id': report.id}