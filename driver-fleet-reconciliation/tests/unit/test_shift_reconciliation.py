from datetime import date, datetime
from unittest.mock import MagicMock, patch

from app.models.output.daily_summary import SummaryStatus
from app.reconciliation.shift_reconciliation import reconcile_shift


def test_shift_reconciliation_matches():
    db = MagicMock()

    # Ground-truth shift
    shift = MagicMock()
    shift.login_time = datetime(2026, 8, 1, 9, 0)
    shift.logout_time = datetime(2026, 8, 1, 17, 0)

    # Raw login event
    login_event = MagicMock()
    login_event.event_time = datetime(2026, 8, 1, 9, 5)

    # Raw logout event
    logout_event = MagicMock()
    logout_event.event_time = datetime(2026, 8, 1, 17, 5)

    # Summary
    summary = MagicMock()
    summary.id = 1
    summary.driver_id = 1
    summary.summary_date = date(2026, 8, 1)

    # Mock database queries
    shift_query = MagicMock()
    shift_query.filter.return_value.first.return_value = shift

    login_query = MagicMock()
    login_query.filter.return_value.order_by.return_value.first.return_value = login_event

    logout_query = MagicMock()
    logout_query.filter.return_value.order_by.return_value.first.return_value = logout_event

    db.query.side_effect = [
        shift_query,
        login_query,
        logout_query,
    ]

    reconcile_shift(
        db=db,
        driver_id=1,
        summary_date=date(2026, 8, 1),
        summary=summary,
    )

    assert summary.status == SummaryStatus.RESOLVED


def test_shift_reconciliation_mismatch():
    db = MagicMock()

    # Ground-truth shift
    shift = MagicMock()
    shift.login_time = datetime(2026, 8, 1, 9, 0)
    shift.logout_time = datetime(2026, 8, 1, 17, 0)

    # Raw events are 30 minutes late
    login_event = MagicMock()
    login_event.event_time = datetime(2026, 8, 1, 9, 30)

    logout_event = MagicMock()
    logout_event.event_time = datetime(2026, 8, 1, 17, 30)

    # Summary
    summary = MagicMock()
    summary.id = 1
    summary.driver_id = 1
    summary.summary_date = date(2026, 8, 1)

    # Mock database queries
    shift_query = MagicMock()
    shift_query.filter.return_value.first.return_value = shift

    login_query = MagicMock()
    login_query.filter.return_value.order_by.return_value.first.return_value = login_event

    logout_query = MagicMock()
    logout_query.filter.return_value.order_by.return_value.first.return_value = logout_event

    db.query.side_effect = [
        shift_query,
        login_query,
        logout_query,
    ]

    # We only want to test shift reconciliation here.
    # Exception creation is tested separately.
    with patch(
        "app.reconciliation.shift_reconciliation.create_exception"
    ) as mock_create_exception:

        reconcile_shift(
            db=db,
            driver_id=1,
            summary_date=date(2026, 8, 1),
            summary=summary,
        )

    assert summary.status == SummaryStatus.REVIEW_REQUIRED
    mock_create_exception.assert_called_once()