from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.output.daily_summary import DailySummary
from app.schemas.daily_summary import DailySummaryResponse

router = APIRouter(
    prefix="/summaries",
    tags=["Summaries"],
)


@router.get(
    "/{summary_date}",
    response_model=list[DailySummaryResponse],
)
def get_summaries(
    summary_date: date,
    db: Session = Depends(get_db),
):
    return (
        db.query(DailySummary)
        .filter(DailySummary.summary_date == summary_date)
        .order_by(DailySummary.driver_id)
        .all()
    )


@router.get(
    "/{summary_date}/{driver_id}",
    response_model=DailySummaryResponse,
)
def get_driver_summary(
    summary_date: date,
    driver_id: int,
    db: Session = Depends(get_db),
):
    summary = (
        db.query(DailySummary)
        .filter(
            DailySummary.driver_id == driver_id,
            DailySummary.summary_date == summary_date,
        )
        .first()
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Daily summary not found",
        )

    return summary