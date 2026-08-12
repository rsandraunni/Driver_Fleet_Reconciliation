from datetime import date

from app.config.database import SessionLocal

from app.models import (
    Driver,
    Vehicle,
    Assignment,
    Shift,
    Trip,
    ShiftEvent,
    DispatchEvent,
    GpsPing,
    FuelSwipe,
)

from app.generator.driver_generator import generate_drivers
from app.generator.vehicle_generator import generate_vehicles
from app.generator.assignment_generator import generate_assignments
from app.generator.shift_generator import generate_shifts
from app.generator.trip_generator import generate_trips

from app.generator.shift_event_generator import generate_shift_events
from app.generator.dispatch_event_generator import generate_dispatch_events
from app.generator.gps_generator import generate_gps_pings
from app.generator.fuel_swipe_generator import generate_fuel_swipes


def main():

    session = SessionLocal()

    try:

        print("Clearing existing data...")

        session.query(FuelSwipe).delete()
        session.query(GpsPing).delete()
        session.query(DispatchEvent).delete()
        session.query(ShiftEvent).delete()

        session.query(Trip).delete()
        session.query(Shift).delete()
        session.query(Assignment).delete()

        session.query(Vehicle).delete()
        session.query(Driver).delete()

        session.commit()

        print("Generating drivers...")
        drivers = generate_drivers(20)

        print("Generating vehicles...")
        vehicles = generate_vehicles(20)

        print("Generating assignments...")
        assignments = generate_assignments(
            drivers,
            vehicles,
            start_date=date(2026, 8, 1),
            num_days=7,
        )

        print("Generating shifts...")
        shifts = generate_shifts(
            drivers,
            start_date=date(2026, 8, 1),
            num_days=7,
        )

        print("Generating trips...")
        trips = generate_trips(assignments)

        print("Generating shift events...")
        shift_events = generate_shift_events(shifts)

        print("Generating dispatch events...")
        dispatch_events = generate_dispatch_events(trips)

        print("Generating GPS pings...")
        gps_pings = generate_gps_pings(trips)

        print("Generating fuel swipes...")
        fuel_swipes = generate_fuel_swipes(trips)

        session.add_all(drivers)
        session.add_all(vehicles)
        session.add_all(assignments)
        session.add_all(shifts)
        session.add_all(trips)

        session.add_all(shift_events)
        session.add_all(dispatch_events)
        session.add_all(gps_pings)
        session.add_all(fuel_swipes)

        session.commit()

        print("\n========== SUMMARY ==========")
        print(f"Drivers           : {len(drivers)}")
        print(f"Vehicles          : {len(vehicles)}")
        print(f"Assignments       : {len(assignments)}")
        print(f"Shifts            : {len(shifts)}")
        print(f"Trips             : {len(trips)}")
        print(f"Shift Events      : {len(shift_events)}")
        print(f"Dispatch Events   : {len(dispatch_events)}")
        print(f"GPS Pings         : {len(gps_pings)}")
        print(f"Fuel Swipes       : {len(fuel_swipes)}")
        print("=============================")

        print("\nData generation completed successfully!")

    except Exception as e:
        session.rollback()
        print(f"\nError: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    main()