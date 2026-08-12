import random
from datetime import timedelta

from app.models.ground_truth.trip import Trip
from app.models.raw_input.fuel_swipe import FuelSwipe


def generate_fuel_swipes(
    trips: list[Trip],
) -> list[FuelSwipe]:

    swipes = []

    for trip in trips:

        if random.random() < 0.35:

            swipes.append(
                FuelSwipe(
                    driver=trip.driver,
                    vehicle=trip.vehicle,
                    timestamp=trip.actual_start + timedelta(
                        minutes=random.randint(10, 60)
                    ),
                    amount=round(
                        random.uniform(20, 70),
                        2,
                    ),
                )
            )

    return swipes