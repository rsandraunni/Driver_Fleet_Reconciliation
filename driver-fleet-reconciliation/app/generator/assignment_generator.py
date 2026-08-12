from datetime import date, timedelta
import random

from app.models.ground_truth.assignment import Assignment
from app.models.ground_truth.driver import Driver
from app.models.ground_truth.vehicle import Vehicle


def generate_assignments(
    drivers: list[Driver],
    vehicles: list[Vehicle],
    start_date: date,
    num_days: int,
) -> list[Assignment]:
    """
    Generate one driver-to-vehicle assignment per day.
    """

    assignments = []

    current_date = start_date

    for _ in range(num_days):

        # Shuffle vehicles so assignments change every day
        available_vehicles = vehicles.copy()
        random.shuffle(available_vehicles)

        for driver, vehicle in zip(drivers, available_vehicles):

            assignments.append(
                Assignment(
                    driver=driver,
                    vehicle=vehicle,
                    assignment_date=current_date,
                )
            )

        current_date += timedelta(days=1)

    return assignments