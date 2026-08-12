from datetime import date

from sqlalchemy.orm import Session

from app.models.ground_truth.trip import Trip
from app.models.raw_input.dispatch_event import (
    DispatchEvent,
    DispatchEventType,
)


def reconcile_dispatch(
    db: Session,
    driver_id: int,
    summary_date: date,
):
    # Get ground-truth trips for the driver and date
    trips = (
        db.query(Trip)
        .filter(
            Trip.driver_id == driver_id,
            Trip.trip_date == summary_date,
        )
        .all()
    )

    results = []

    for trip in trips:

        # Check for TRIP_ASSIGNED event
        assigned_event = (
            db.query(DispatchEvent)
            .filter(
                DispatchEvent.driver_id == driver_id,
                DispatchEvent.trip_id == trip.trip_id,
                DispatchEvent.event_type
                == DispatchEventType.TRIP_ASSIGNED,
            )
            .first()
        )

        # Check for TRIP_COMPLETED event
        completed_event = (
            db.query(DispatchEvent)
            .filter(
                DispatchEvent.driver_id == driver_id,
                DispatchEvent.trip_id == trip.trip_id,
                DispatchEvent.event_type
                == DispatchEventType.TRIP_COMPLETED,
            )
            .first()
        )

        # Both events exist
        if assigned_event and completed_event:
            results.append(
                {
                    "trip_id": trip.trip_id,
                    "status": "RESOLVED",
                    "reason": "DISPATCH_MATCHED",
                }
            )

        # One or both events are missing
        else:
            results.append(
                {
                    "trip_id": trip.trip_id,
                    "status": "REVIEW_REQUIRED",
                    "reason": "MISSING_DISPATCH_EVENT",
                }
            )

    return results