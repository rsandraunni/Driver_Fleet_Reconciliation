from datetime import date, datetime

from app.models.ground_truth.driver import Driver
from app.models.ground_truth.vehicle import Vehicle
from app.models.ground_truth.shift import Shift
from app.models.ground_truth.trip import Trip

from app.models.raw_input.shift_event import (
    ShiftEvent,
    ShiftEventType,
)

from app.models.raw_input.dispatch_event import (
    DispatchEvent,
    DispatchEventType,
)

from app.models.raw_input.gps_ping import GpsPing

from app.models.output.daily_summary import SummaryStatus

from app.reconciliation.engine import reconcile_driver_day


def test_full_reconciliation_flow(db):
    # --------------------------------------------------
    # 1. Create ground-truth driver and vehicle
    # --------------------------------------------------

    driver = Driver(
        driver_id="DRVTEST01",
        name="Test Driver",
    )

    vehicle = Vehicle(
        vehicle_id="VEHTEST01",
        registration_number="KLTEST01",
    )

    db.add(driver)
    db.add(vehicle)
    db.commit()

    # --------------------------------------------------
    # 2. Create ground-truth shift
    # --------------------------------------------------

    shift = Shift(
        driver_id=driver.id,
        shift_date=date(2026, 8, 1),
        login_time=datetime(2026, 8, 1, 9, 0),
        logout_time=datetime(2026, 8, 1, 17, 0),
    )

    db.add(shift)
    db.commit()

    # --------------------------------------------------
    # 3. Create ground-truth trip
    # --------------------------------------------------

    trip = Trip(
        trip_id="TRIPTEST01",
        driver_id=driver.id,
        vehicle_id=vehicle.id,
        trip_date=date(2026, 8, 1),

        planned_start=datetime(2026, 8, 1, 9, 30),
        planned_end=datetime(2026, 8, 1, 11, 30),

        actual_start=datetime(2026, 8, 1, 9, 30),
        actual_end=datetime(2026, 8, 1, 11, 30),

        distance_km=50.0,
    )

    db.add(trip)
    db.commit()

    # --------------------------------------------------
    # 4. Create raw shift events
    # --------------------------------------------------

    shift_events = [
        ShiftEvent(
            driver_id=driver.id,
            event_type=ShiftEventType.LOGIN,
            event_time=datetime(2026, 8, 1, 8, 57),
        ),
        ShiftEvent(
            driver_id=driver.id,
            event_type=ShiftEventType.LOGOUT,
            event_time=datetime(2026, 8, 1, 17, 2),
        ),
    ]

    db.add_all(shift_events)

    # --------------------------------------------------
    # 5. Create raw dispatch events
    # --------------------------------------------------

    dispatch_events = [
        DispatchEvent(
            trip_id="TRIPTEST01",
            driver_id=driver.id,
            event_type=DispatchEventType.TRIP_ASSIGNED,
            event_time=datetime(2026, 8, 1, 9, 30),
        ),
        DispatchEvent(
            trip_id="TRIPTEST01",
            driver_id=driver.id,
            event_type=DispatchEventType.TRIP_COMPLETED,
            event_time=datetime(2026, 8, 1, 11, 30),
        ),
    ]

    db.add_all(dispatch_events)

    # --------------------------------------------------
    # 6. Create raw GPS data
    # --------------------------------------------------

    gps_ping = GpsPing(
        vehicle_id=vehicle.id,
        timestamp=datetime(2026, 8, 1, 10, 0),
        latitude=8.5241,
        longitude=76.9366,
    )

    db.add(gps_ping)

    # No fuel swipe is created intentionally.
    # This should produce RESOLVED_WITH_FLAGS.

    db.commit()

    # --------------------------------------------------
    # 7. Run complete reconciliation
    # --------------------------------------------------

    summary = reconcile_driver_day(
        db=db,
        driver_id=driver.id,
        summary_date=date(2026, 8, 1),
    )

    # --------------------------------------------------
    # 8. Verify final summary
    # --------------------------------------------------

    assert summary.driver_id == driver.id
    assert summary.summary_date == date(2026, 8, 1)

    assert summary.hours_on_duty == 8.0
    assert summary.trips_completed == 1
    assert summary.distance_km == 50.0

    assert summary.status == SummaryStatus.RESOLVED_WITH_FLAGS