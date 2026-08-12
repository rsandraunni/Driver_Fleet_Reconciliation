from datetime import date, datetime
from unittest.mock import MagicMock

from app.reconciliation.fuel_reconciliation import reconcile_fuel


def create_trip():
    trip = MagicMock()
    trip.trip_id = "TRIP00001"
    trip.vehicle_id = 1
    trip.actual_start = datetime(2026, 8, 1, 8, 0)
    trip.actual_end = datetime(2026, 8, 1, 12, 0)
    return trip


def test_fuel_matched():
    db = MagicMock()

    trip = create_trip()

    fuel_swipe = MagicMock()
    fuel_swipe.driver_id = 1

    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = [trip]

    fuel_query = MagicMock()
    fuel_query.filter.return_value.all.return_value = [fuel_swipe]

    db.query.side_effect = [
        trip_query,
        fuel_query,
    ]

    result = reconcile_fuel(
        db=db,
        driver_id=1,
        summary_date=date(2026, 8, 1),
    )

    assert result[0]["trip_id"] == "TRIP00001"
    assert result[0]["status"] == "RESOLVED"
    assert result[0]["reason"] == "FUEL_MATCHED"
    assert result[0]["fuel_swipe_count"] == 1


def test_fuel_driver_mismatch():
    db = MagicMock()

    trip = create_trip()

    fuel_swipe = MagicMock()
    fuel_swipe.driver_id = 20

    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = [trip]

    fuel_query = MagicMock()
    fuel_query.filter.return_value.all.return_value = [fuel_swipe]

    db.query.side_effect = [
        trip_query,
        fuel_query,
    ]

    result = reconcile_fuel(
        db=db,
        driver_id=1,
        summary_date=date(2026, 8, 1),
    )

    assert result[0]["trip_id"] == "TRIP00001"
    assert result[0]["status"] == "REVIEW_REQUIRED"
    assert result[0]["reason"] == "FUEL_DRIVER_MISMATCH"
    assert result[0]["fuel_swipe_count"] == 1


def test_no_fuel_swipe():
    db = MagicMock()

    trip = create_trip()

    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = [trip]

    fuel_query = MagicMock()
    fuel_query.filter.return_value.all.return_value = []

    db.query.side_effect = [
        trip_query,
        fuel_query,
    ]

    result = reconcile_fuel(
        db=db,
        driver_id=1,
        summary_date=date(2026, 8, 1),
    )

    assert result[0]["trip_id"] == "TRIP00001"
    assert result[0]["status"] == "RESOLVED_WITH_FLAGS"
    assert result[0]["reason"] == "NO_FUEL_SWIPE"
    assert result[0]["fuel_swipe_count"] == 0