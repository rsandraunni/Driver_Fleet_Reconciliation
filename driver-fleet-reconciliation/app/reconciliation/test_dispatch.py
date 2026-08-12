from datetime import date

from app.config.database import SessionLocal
from app.reconciliation.dispatch_reconciliation import reconcile_dispatch


def main():
    db = SessionLocal()

    try:
        results = reconcile_dispatch(
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