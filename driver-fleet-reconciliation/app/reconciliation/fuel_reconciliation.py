from datetime import date

from sqlalchemy.orm import Session

from app.models.ground_truth.trip import Trip
from app.models.raw_input.fuel_swipe import FuelSwipe


def reconcile_fuel(
    db: Session,
    driver_id: int,
    summary_date: date,
):
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

        fuel_swipes = (
            db.query(FuelSwipe)
            .filter(
                FuelSwipe.vehicle_id == trip.vehicle_id,
                FuelSwipe.timestamp >= trip.actual_start,
                FuelSwipe.timestamp <= trip.actual_end,
            )
            .all()
        )

        # Fuel swipe found for the trip vehicle
        if fuel_swipes:

            wrong_driver = any(
                swipe.driver_id != driver_id
                for swipe in fuel_swipes
            )

            if wrong_driver:
                results.append(
                    {
                        "trip_id": trip.trip_id,
                        "status": "REVIEW_REQUIRED",
                        "reason": "FUEL_DRIVER_MISMATCH",
                        "fuel_swipe_count": len(fuel_swipes),
                    }
                )

            else:
                results.append(
                    {
                        "trip_id": trip.trip_id,
                        "status": "RESOLVED",
                        "reason": "FUEL_MATCHED",
                        "fuel_swipe_count": len(fuel_swipes),
                    }
                )

        # No fuel swipe is not automatically an error
        else:
            results.append(
                {
                    "trip_id": trip.trip_id,
                    "status": "RESOLVED_WITH_FLAGS",
                    "reason": "NO_FUEL_SWIPE",
                    "fuel_swipe_count": 0,
                }
            )

    return results