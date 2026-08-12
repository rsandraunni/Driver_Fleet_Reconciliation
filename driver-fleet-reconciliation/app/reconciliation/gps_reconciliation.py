from datetime import date

from sqlalchemy.orm import Session

from app.models.ground_truth.trip import Trip
from app.models.raw_input.gps_ping import GpsPing


def reconcile_gps(
    db: Session,
    driver_id: int,
    summary_date: date,
):
    # Get ground-truth trips
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

        # Find GPS pings for the vehicle during the trip
        gps_count = (
            db.query(GpsPing)
            .filter(
                GpsPing.vehicle_id == trip.vehicle_id,
                GpsPing.timestamp >= trip.actual_start,
                GpsPing.timestamp <= trip.actual_end,
            )
            .count()
        )

        if gps_count > 0:
            results.append(
                {
                    "trip_id": trip.trip_id,
                    "status": "RESOLVED",
                    "reason": "GPS_DATA_FOUND",
                    "gps_ping_count": gps_count,
                }
            )

        else:
            results.append(
                {
                    "trip_id": trip.trip_id,
                    "status": "REVIEW_REQUIRED",
                    "reason": "MISSING_GPS_DATA",
                    "gps_ping_count": 0,
                }
            )

    return results