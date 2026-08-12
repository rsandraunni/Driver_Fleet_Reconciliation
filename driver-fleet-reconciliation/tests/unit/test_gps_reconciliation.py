from datetime import date, datetime
from unittest.mock import MagicMock

from app.reconciliation.gps_reconciliation import reconcile_gps


def test_gps_data_found():
    db = MagicMock()

    # Ground-truth trip
    trip = MagicMock()
    trip.trip_id = "TRIP00001"
    trip.vehicle_id = 1
    trip.actual_start = datetime(2026, 8, 1, 8, 0)
    trip.actual_end = datetime(2026, 8, 1, 12, 0)

    # First query returns the trip
    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = [trip]

    # Second query counts GPS pings
    gps_query = MagicMock()
    gps_query.filter.return_value.count.return_value = 50

    db.query.side_effect = [
        trip_query,
        gps_query,
    ]

    result = reconcile_gps(
        db=db,
        driver_id=1,
        summary_date=date(2026, 8, 1),
    )

    assert len(result) == 1
    assert result[0]["trip_id"] == "TRIP00001"
    assert result[0]["status"] == "RESOLVED"
    assert result[0]["reason"] == "GPS_DATA_FOUND"
    assert result[0]["gps_ping_count"] == 50


def test_gps_data_missing():
    db = MagicMock()

    # Ground-truth trip
    trip = MagicMock()
    trip.trip_id = "TRIP00001"
    trip.vehicle_id = 1
    trip.actual_start = datetime(2026, 8, 1, 8, 0)
    trip.actual_end = datetime(2026, 8, 1, 12, 0)

    # First query returns the trip
    trip_query = MagicMock()
    trip_query.filter.return_value.all.return_value = [trip]

    # Second query finds no GPS pings
    gps_query = MagicMock()
    gps_query.filter.return_value.count.return_value = 0

    db.query.side_effect = [
        trip_query,
        gps_query,
    ]

    result = reconcile_gps(
        db=db,
        driver_id=1,
        summary_date=date(2026, 8, 1),
    )

    assert len(result) == 1
    assert result[0]["trip_id"] == "TRIP00001"
    assert result[0]["status"] == "REVIEW_REQUIRED"
    assert result[0]["reason"] == "MISSING_GPS_DATA"
    assert result[0]["gps_ping_count"] == 0