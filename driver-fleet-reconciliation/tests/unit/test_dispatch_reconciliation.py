from datetime import date
from unittest.mock import MagicMock

from app.reconciliation.dispatch_reconciliation import reconcile_dispatch


def create_trip():
    trip = MagicMock()
    trip.trip_id = "TRIP00001"
    return trip


def test_dispatch_matched():
    db = MagicMock()

    trip = create_trip()

    assigned_event = MagicMock()
    completed_event = MagicMock()

    # First query -> trips
    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = [trip]

    # Second query -> assigned event
    assigned_query = MagicMock()
    assigned_query.filter.return_value.first.return_value = assigned_event

    # Third query -> completed event
    completed_query = MagicMock()
    completed_query.filter.return_value.first.return_value = completed_event

    db.query.side_effect = [
        trip_query,
        assigned_query,
        completed_query,
    ]

    result = reconcile_dispatch(
        db=db,
        driver_id=1,
        summary_date=date(2026, 8, 1),
    )

    assert result[0]["trip_id"] == "TRIP00001"
    assert result[0]["status"] == "RESOLVED"
    assert result[0]["reason"] == "DISPATCH_MATCHED"


def test_dispatch_event_missing():
    db = MagicMock()

    trip = create_trip()

    assigned_event = MagicMock()

    # First query -> trips
    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = [trip]

    # Second query -> assigned event exists
    assigned_query = MagicMock()
    assigned_query.filter.return_value.first.return_value = assigned_event

    # Third query -> completed event missing
    completed_query = MagicMock()
    completed_query.filter.return_value.first.return_value = None

    db.query.side_effect = [
        trip_query,
        assigned_query,
        completed_query,
    ]

    result = reconcile_dispatch(
        db=db,
        driver_id=1,
        summary_date=date(2026, 8, 1),
    )

    assert result[0]["trip_id"] == "TRIP00001"
    assert result[0]["status"] == "REVIEW_REQUIRED"
    assert result[0]["reason"] == "MISSING_DISPATCH_EVENT"