from datetime import date

from sqlalchemy.orm import Session

from app.models.ground_truth.shift import Shift
from app.models.raw_input.shift_event import (
    ShiftEvent,
    ShiftEventType,
)
from app.models.output.daily_summary import (
    DailySummary,
    SummaryStatus,
)
from app.models.output.exception import ExceptionSeverity
from app.reconciliation.exceptions import create_exception


SHIFT_TOLERANCE_MINUTES = 15


def reconcile_shift(
    db: Session,
    driver_id: int,
    summary_date: date,
    summary: DailySummary,
):
    # Get ground-truth shift
    shift = (
        db.query(Shift)
        .filter(
            Shift.driver_id == driver_id,
            Shift.shift_date == summary_date,
        )
        .first()
    )

    # Get raw login event
    login_event = (
        db.query(ShiftEvent)
        .filter(
            ShiftEvent.driver_id == driver_id,
            ShiftEvent.event_type == ShiftEventType.LOGIN,
        )
        .order_by(ShiftEvent.event_time)
        .first()
    )

    # Get raw logout event
    logout_event = (
        db.query(ShiftEvent)
        .filter(
            ShiftEvent.driver_id == driver_id,
            ShiftEvent.event_type == ShiftEventType.LOGOUT,
        )
        .order_by(ShiftEvent.event_time)
        .first()
    )

    # If ground truth shift is missing
    if not shift:
        create_exception(
            db=db,
            summary=summary,
            reason_code="SHIFT_NOT_FOUND",
            severity=ExceptionSeverity.BLOCKING,
            message="Ground-truth shift was not found.",
        )

        summary.status = SummaryStatus.REVIEW_REQUIRED
        db.commit()
        return

    # If raw events are missing
    if not login_event or not logout_event:
        create_exception(
            db=db,
            summary=summary,
            reason_code="SHIFT_EVENT_MISSING",
            severity=ExceptionSeverity.BLOCKING,
            message="Login or logout event is missing from raw shift events.",
        )

        summary.status = SummaryStatus.REVIEW_REQUIRED
        db.commit()
        return

    # Calculate differences
    login_difference = abs(
        (shift.login_time - login_event.event_time).total_seconds()
    ) / 60

    logout_difference = abs(
        (shift.logout_time - logout_event.event_time).total_seconds()
    ) / 60

    # Check tolerance
    if (
        login_difference > SHIFT_TOLERANCE_MINUTES
        or logout_difference > SHIFT_TOLERANCE_MINUTES
    ):
        create_exception(
            db=db,
            summary=summary,
            reason_code="SHIFT_TIME_MISMATCH",
            severity=ExceptionSeverity.BLOCKING,
            message="Shift login or logout time differs from raw event beyond the allowed tolerance.",
        )

        summary.status = SummaryStatus.REVIEW_REQUIRED
        db.commit()
        return

    #print("Shift reconciliation successful.")
    summary.status = SummaryStatus.RESOLVED

    db.commit()
    db.refresh(summary)

    print("Shift reconciliation successful.")