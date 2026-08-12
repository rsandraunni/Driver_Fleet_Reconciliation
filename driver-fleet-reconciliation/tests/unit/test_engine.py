from datetime import date
from unittest.mock import MagicMock, patch

from app.models.output.daily_summary import SummaryStatus
from app.reconciliation.engine import reconcile_driver_day


def create_summary():
    summary = MagicMock()
    summary.id = 1
    summary.driver_id = 1
    summary.summary_date = date(2026, 8, 1)
    summary.status = SummaryStatus.RESOLVED
    return summary


def test_engine_all_reconciliations_resolved():
    db = MagicMock()

    # No existing summary
    summary_query = MagicMock()
    summary_query.filter.return_value.first.return_value = None

    shift_query = MagicMock()
    shift_query.filter.return_value.first.return_value = None

    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = []

    db.query.side_effect = [
        shift_query,
        trip_query,
        summary_query,
    ]

    with patch(
        "app.reconciliation.engine.reconcile_shift"
    ) as mock_shift, patch(
        "app.reconciliation.engine.reconcile_dispatch"
    ) as mock_dispatch, patch(
        "app.reconciliation.engine.reconcile_gps"
    ) as mock_gps, patch(
        "app.reconciliation.engine.reconcile_fuel"
    ) as mock_fuel:

        mock_shift.return_value = {
            "status": "RESOLVED"
        }

        mock_dispatch.return_value = []

        mock_gps.return_value = []

        mock_fuel.return_value = []

        result = reconcile_driver_day(
            db=db,
            driver_id=1,
            summary_date=date(2026, 8, 1),
        )

    assert result.status == SummaryStatus.RESOLVED


def test_engine_fuel_flag_results_in_resolved_with_flags():
    db = MagicMock()

    summary_query = MagicMock()
    summary_query.filter.return_value.first.return_value = None

    shift_query = MagicMock()
    shift_query.filter.return_value.first.return_value = None

    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = []

    db.query.side_effect = [
        shift_query,
        trip_query,
        summary_query,
    ]

    with patch(
        "app.reconciliation.engine.reconcile_shift"
    ) as mock_shift, patch(
        "app.reconciliation.engine.reconcile_dispatch"
    ) as mock_dispatch, patch(
        "app.reconciliation.engine.reconcile_gps"
    ) as mock_gps, patch(
        "app.reconciliation.engine.reconcile_fuel"
    ) as mock_fuel:

        mock_shift.return_value = {
            "status": "RESOLVED"
        }

        mock_dispatch.return_value = []

        mock_gps.return_value = []

        mock_fuel.return_value = [
            {
                "trip_id": "TRIP00001",
                "status": "RESOLVED_WITH_FLAGS",
                "reason": "NO_FUEL_SWIPE",
            }
        ]

        result = reconcile_driver_day(
            db=db,
            driver_id=1,
            summary_date=date(2026, 8, 1),
        )

    assert result.status == SummaryStatus.RESOLVED_WITH_FLAGS


def test_engine_blocking_failure_results_in_review_required():
    db = MagicMock()

    summary_query = MagicMock()
    summary_query.filter.return_value.first.return_value = None

    shift_query = MagicMock()
    shift_query.filter.return_value.first.return_value = None

    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = []

    db.query.side_effect = [
        shift_query,
        trip_query,
        summary_query,
    ]

    with patch(
        "app.reconciliation.engine.reconcile_shift"
    ) as mock_shift, patch(
        "app.reconciliation.engine.reconcile_dispatch"
    ) as mock_dispatch, patch(
        "app.reconciliation.engine.reconcile_gps"
    ) as mock_gps, patch(
        "app.reconciliation.engine.reconcile_fuel"
    ) as mock_fuel, patch(
        "app.reconciliation.engine.create_exception"
    ):

        mock_shift.return_value = {
            "status": "REVIEW_REQUIRED",
            "reason": "SHIFT_TIME_MISMATCH",
        }

        mock_dispatch.return_value = []
        mock_gps.return_value = []
        mock_fuel.return_value = []

        result = reconcile_driver_day(
            db=db,
            driver_id=1,
            summary_date=date(2026, 8, 1),
        )

    assert result.status == SummaryStatus.REVIEW_REQUIRED