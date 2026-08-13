'''
from datetime import date

from sqlalchemy.orm import Session

from app.models.output.daily_summary import DailySummary
from app.models.output.exception import (
    ReconciliationException,
    ExceptionSeverity,
)


def create_exception(
    db: Session,
    summary: DailySummary,
    reason_code: str,
    severity: ExceptionSeverity,
    message: str,
):
    exception = ReconciliationException(
        summary_id=summary.id,
        driver_id=summary.driver_id,
        exception_date=summary.summary_date,
        reason_code=reason_code,
        severity=severity,
        message=message,
    )

    db.add(exception)
    db.commit()
    db.refresh(exception)

    return exception
'''

from sqlalchemy.orm import Session

from app.models.output.daily_summary import DailySummary
from app.models.output.exception import (
    ExceptionSeverity,
    ReconciliationException,
)


def create_exception(
    db: Session,
    summary: DailySummary,
    reason_code: str,
    severity: ExceptionSeverity,
    message: str,
):
    existing = (
        db.query(ReconciliationException)
        .filter(
            ReconciliationException.summary_id == summary.id,
            ReconciliationException.reason_code == reason_code,
            ReconciliationException.message == message,
        )
        .first()
    )

    if existing:
        return existing

    exception = ReconciliationException(
        summary_id=summary.id,
        driver_id=str(summary.driver_id),
        exception_date=summary.summary_date,
        reason_code=reason_code,
        severity=severity,
        message=message,
    )

    db.add(exception)
    db.commit()
    db.refresh(exception)

    return exception