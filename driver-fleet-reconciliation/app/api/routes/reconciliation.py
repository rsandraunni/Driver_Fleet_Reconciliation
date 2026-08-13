from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.reconciliation.engine import reconcile_driver_day
from app.schemas.daily_summary import DailySummaryResponse


router = APIRouter(
    prefix="/reconcile",
    tags=["Reconciliation"],
)


@router.post(
    "/{driver_id}/{summary_date}",
    response_model=DailySummaryResponse,
)
def reconcile(
    driver_id: int,
    summary_date: date,
    db: Session = Depends(get_db),
):
    summary = reconcile_driver_day(
        db=db,
        driver_id=driver_id,
        summary_date=summary_date,
    )

    return summary