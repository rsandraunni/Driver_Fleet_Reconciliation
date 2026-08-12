from datetime import datetime, timedelta
import random

from app.models.ground_truth.trip import Trip
from app.models.ground_truth.assignment import Assignment


def generate_trips(
    assignments: list[Assignment],
) -> list[Trip]:

    trips = []

    trip_number = 1

    for assignment in assignments:

        start_hour = random.randint(7, 10)

        planned_start = datetime.combine(
            assignment.assignment_date,
            datetime.min.time()
        ) + timedelta(hours=start_hour)

        trip_duration = random.randint(2, 5)

        planned_end = planned_start + timedelta(
            hours=trip_duration
        )

        actual_start = planned_start + timedelta(
            minutes=random.randint(-10, 10)
        )

        actual_end = planned_end + timedelta(
            minutes=random.randint(-10, 20)
        )

        distance = round(
            random.uniform(30, 200),
            2
        )

        trips.append(
            Trip(
                trip_id=f"TRIP{trip_number:05d}",
                driver=assignment.driver,
                vehicle=assignment.vehicle,
                trip_date=assignment.assignment_date,
                planned_start=planned_start,
                planned_end=planned_end,
                actual_start=actual_start,
                actual_end=actual_end,
                distance_km=distance,
            )
        )

        trip_number += 1

    return trips