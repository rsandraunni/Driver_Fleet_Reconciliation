'''
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
        print("Date:", summary.summary_date)
        print("Hours on duty:", summary.hours_on_duty)
        print("Trips completed:", summary.trips_completed)
        print("Distance:", summary.distance_km)
        print("Status:", summary.status.value)

    finally:
        db.close()


if __name__ == "__main__":
    main()
'''

from datetime import date

from app.config.database import SessionLocal
from app.reconciliation.engine import reconcile_shift


def main():
    db = SessionLocal()

    try:
        result = reconcile_shift(
            db=db,
            driver_id=1,
            summary_date=date(2026, 8, 1),
        )

        print("Shift reconciliation result:")
        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    main()