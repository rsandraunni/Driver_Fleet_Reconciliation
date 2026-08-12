from datetime import date

from app.config.database import SessionLocal
from app.models.output.daily_summary import DailySummary
from app.models.output.exception import ExceptionSeverity
from app.reconciliation.exceptions import create_exception


def main():
    db = SessionLocal()

    try:
        summary = (
            db.query(DailySummary)
            .filter(
                DailySummary.driver_id == 1,
                DailySummary.summary_date == date(2026, 8, 1),
            )
            .first()
        )

        if not summary:
            print("Daily summary not found.")
            return

        exception = create_exception(
            db=db,
            summary=summary,
            reason_code="SHIFT_TIME_MISMATCH",
            severity=ExceptionSeverity.BLOCKING,
            message="Shift login or logout time differs from raw event beyond the allowed tolerance.",
        )

        print("Exception created successfully!")
        print("Exception ID:", exception.id)
        print("Reason:", exception.reason_code)
        print("Severity:", exception.severity.value)

    finally:
        db.close()


if __name__ == "__main__":
    main()