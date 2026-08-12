from datetime import date

from app.config.database import SessionLocal
from app.reconciliation.gps_reconciliation import reconcile_gps


def main():
    db = SessionLocal()

    try:
        results = reconcile_gps(
            db=db,
            driver_id=1,
            summary_date=date(2026, 8, 1),
        )

        for result in results:
            print(result)

    finally:
        db.close()


if __name__ == "__main__":
    main()