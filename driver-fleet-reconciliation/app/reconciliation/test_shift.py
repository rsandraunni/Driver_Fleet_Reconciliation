from datetime import date

from app.config.database import SessionLocal
from app.reconciliation.engine import reconcile_driver_day


def main():
    db = SessionLocal()

    try:
        summary = reconcile_driver_day(
            db=db,
            driver_id=1,
            summary_date=date(2026, 8, 1),
        )

        print("Reconciliation completed!")
        print("Summary ID:", summary.id)
        print("Driver ID:", summary.driver_id)
        print("Status:", summary.status.value)
        print("Hours:", summary.hours_on_duty)
        print("Trips:", summary.trips_completed)
        print("Distance:", summary.distance_km)

    finally:
        db.close()


if __name__ == "__main__":
    main()