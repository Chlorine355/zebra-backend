from fastapi import APIRouter, Depends, HTTPException, status, Form
from auth.dependencies import create_report, get_current_user, get_db, get_report, get_reports, get_stats
from const import MAX_DAILY_REPORTS
from .schemas import ReportCreate, ReportCreateResponse, ReportFull, ReportsShortResponse, Stats
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/all", response_model=ReportsShortResponse)
def reports_all(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    reports = get_reports(db, user=current_user)
    return {'reports': reports}

@router.get("/one_by_id", response_model=ReportFull)
def report_one_by_id(report_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    report = get_report(db, current_user, report_id=report_id)
    return report

@router.post("/create", response_model=ReportCreateResponse)
async def reports_create(report: ReportCreate = Form(), current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.daily_reports >= MAX_DAILY_REPORTS:
        raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Достигнут лимит обращений за день",
        headers={"WWW-Authenticate": "Bearer"},
    )
    report = await create_report(db, report, current_user)
    return {'report_id': report.id}

@router.get("/stats", response_model=Stats)
def stats(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    stat_tuples = get_stats(db, current_user)
    return dict(stat_tuples)