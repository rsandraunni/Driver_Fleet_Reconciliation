from app.reconciliation.shift_reconciliation import reconcile_shift
from app.reconciliation.dispatch_reconciliation import reconcile_dispatch
from app.reconciliation.gps_reconciliation import reconcile_gps
from app.reconciliation.fuel_reconciliation import reconcile_fuel
from app.reconciliation.exceptions import create_exception

from app.models.output.daily_summary import (
    DailySummary,
    SummaryStatus,
)
from app.models.output.exception import ExceptionSeverity


from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.ground_truth.shift import Shift
from app.models.ground_truth.trip import Trip
from app.models.raw_input.shift_event import (
    ShiftEvent,
    ShiftEventType,
)
from app.models.output.daily_summary import (
    DailySummary,
    SummaryStatus,
)


def reconcile_driver_day(
    db: Session,
    driver_id: int,
    summary_date: date,
) -> DailySummary:

    # Get the driver's shift for the day
    shift = (
        db.query(Shift)
        .filter(
            Shift.driver_id == driver_id,
            Shift.shift_date == summary_date,
        )
        .first()
    )

    # Get the driver's trips for the day
    trips = (
        db.query(Trip)
        .filter(
            Trip.driver_id == driver_id,
            Trip.trip_date == summary_date,
        )
        .all()
    )

    # Calculate hours on duty
    hours_on_duty = None

    if shift:
        duration = shift.logout_time - shift.login_time
        hours_on_duty = duration.total_seconds() / 3600

    # Calculate trip information
    trips_completed = len(trips)

    distance_km = sum(
        trip.distance_km
        for trip in trips
    )

    # Check whether a summary already exists
    summary = (
        db.query(DailySummary)
        .filter(
            DailySummary.driver_id == driver_id,
            DailySummary.summary_date == summary_date,
        )
        .first()
    )

    # Create or update summary
    if summary:
        summary.hours_on_duty = hours_on_duty
        summary.trips_completed = trips_completed
        summary.distance_km = distance_km

    else:
        summary = DailySummary(
            driver_id=driver_id,
            summary_date=summary_date,
            hours_on_duty=hours_on_duty,
            trips_completed=trips_completed,
            distance_km=distance_km,
            status=SummaryStatus.RESOLVED,
        )

        db.add(summary)

    # Save first so the summary gets an ID
    db.commit()
    db.refresh(summary)

    # ==================================================
    # 1. SHIFT RECONCILIATION
    # ==================================================

    shift_result = reconcile_shift(
        db=db,
        driver_id=driver_id,
        summary_date=summary_date,
    )

    # ==================================================
    # 2. DISPATCH RECONCILIATION
    # ==================================================

    dispatch_results = reconcile_dispatch(
        db=db,
        driver_id=driver_id,
        summary_date=summary_date,
    )

    # ==================================================
    # 3. GPS RECONCILIATION
    # ==================================================

    gps_results = reconcile_gps(
        db=db,
        driver_id=driver_id,
        summary_date=summary_date,
    )

    # ==================================================
    # 4. FUEL RECONCILIATION
    # ==================================================

    fuel_results = reconcile_fuel(
        db=db,
        driver_id=driver_id,
        summary_date=summary_date,
    )

    # ==================================================
    # DECISION LOGIC
    # ==================================================

    blocking_issue = False
    informational_flag = False

    # -------------------------------
    # Shift result
    # -------------------------------

    if shift_result["status"] == "REVIEW_REQUIRED":

        blocking_issue = True

        create_exception(
            db=db,
            summary=summary,
            reason_code=shift_result["reason"],
            severity=ExceptionSeverity.BLOCKING,
            message=(
                f"Shift reconciliation failed: "
                f"{shift_result['reason']}"
            ),
        )

    # -------------------------------
    # Dispatch results
    # -------------------------------

    for result in dispatch_results:

        if result["status"] == "REVIEW_REQUIRED":

            blocking_issue = True

            create_exception(
                db=db,
                summary=summary,
                reason_code=result["reason"],
                severity=ExceptionSeverity.BLOCKING,
                message=(
                    f"Dispatch reconciliation failed for "
                    f"{result['trip_id']}: "
                    f"{result['reason']}"
                ),
            )

    # -------------------------------
    # GPS results
    # -------------------------------

    for result in gps_results:

        if result["status"] == "REVIEW_REQUIRED":

            blocking_issue = True

            create_exception(
                db=db,
                summary=summary,
                reason_code=result["reason"],
                severity=ExceptionSeverity.BLOCKING,
                message=(
                    f"GPS reconciliation failed for "
                    f"{result['trip_id']}: "
                    f"{result['reason']}"
                ),
            )

    # -------------------------------
    # Fuel results
    # -------------------------------

    for result in fuel_results:

        if result["status"] == "REVIEW_REQUIRED":

            blocking_issue = True

            create_exception(
                db=db,
                summary=summary,
                reason_code=result["reason"],
                severity=ExceptionSeverity.BLOCKING,
                message=(
                    f"Fuel reconciliation failed for "
                    f"{result['trip_id']}: "
                    f"{result['reason']}"
                ),
            )

        elif result["status"] == "RESOLVED_WITH_FLAGS":

            informational_flag = True

    # ==================================================
    # FINAL SUMMARY STATUS
    # ==================================================

    if blocking_issue:

        summary.status = SummaryStatus.REVIEW_REQUIRED

    elif informational_flag:

        summary.status = SummaryStatus.RESOLVED_WITH_FLAGS

    else:

        summary.status = SummaryStatus.RESOLVED

    db.commit()
    db.refresh(summary)

    return summary

def reconcile_shift(
    db: Session,
    driver_id: int,
    summary_date: date,
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

    # No ground-truth shift
    if not shift:
        return {
            "status": "REVIEW_REQUIRED",
            "reason": "NO_GROUND_TRUTH_SHIFT",
        }

    # Get login event
    login_event = (
        db.query(ShiftEvent)
        .filter(
            ShiftEvent.driver_id == driver_id,
            ShiftEvent.event_type == ShiftEventType.LOGIN,
            ShiftEvent.event_time >= (
                shift.login_time - timedelta(hours=1)
            ),
            ShiftEvent.event_time <= (
                shift.login_time + timedelta(hours=1)
            ),
        )
        .order_by(ShiftEvent.event_time)
        .first()
    )

    # Get logout event
    logout_event = (
        db.query(ShiftEvent)
        .filter(
            ShiftEvent.driver_id == driver_id,
            ShiftEvent.event_type == ShiftEventType.LOGOUT,
            ShiftEvent.event_time >= (
                shift.logout_time - timedelta(hours=1)
            ),
            ShiftEvent.event_time <= (
                shift.logout_time + timedelta(hours=1)
            ),
        )
        .order_by(ShiftEvent.event_time)
        .first()
    )

    # Missing raw event
    if not login_event or not logout_event:
        return {
            "status": "REVIEW_REQUIRED",
            "reason": "MISSING_SHIFT_EVENT",
        }

    # Calculate login difference in minutes
    login_difference = abs(
        (login_event.event_time - shift.login_time).total_seconds()
    ) / 60

    # Calculate logout difference in minutes
    logout_difference = abs(
        (logout_event.event_time - shift.logout_time).total_seconds()
    ) / 60

    # Get configured tolerance
    tolerance = settings.SHIFT_TOLERANCE_MINUTES

    # Check whether both events are within tolerance
    if (
        login_difference <= tolerance
        and logout_difference <= tolerance
    ):
        return {
            "status": "RESOLVED",
            "reason": "SHIFT_MATCHED",
            "login_difference": login_difference,
            "logout_difference": logout_difference,
        }

    # Shift mismatch
    return {
        "status": "REVIEW_REQUIRED",
        "reason": "SHIFT_TIME_MISMATCH",
        "login_difference": login_difference,
        "logout_difference": logout_difference,
    }