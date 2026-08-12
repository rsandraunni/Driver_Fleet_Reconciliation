import random
from datetime import timedelta

from app.models.ground_truth.trip import Trip
from app.models.raw_input.gps_ping import GpsPing


def generate_gps_pings(
    trips: list[Trip],
) -> list[GpsPing]:

    pings = []

    for trip in trips:

        current = trip.actual_start

        while current <= trip.actual_end:

            pings.append(
                GpsPing(
                    vehicle=trip.vehicle,
                    timestamp=current,
                    latitude=8.5 + random.random() / 10,
                    longitude=76.9 + random.random() / 10,
                )
            )

            current += timedelta(minutes=5)

    return pings