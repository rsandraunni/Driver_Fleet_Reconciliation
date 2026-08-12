from app.models.ground_truth.trip import Trip
from app.models.raw_input.dispatch_event import (
    DispatchEvent,
    DispatchEventType,
)


def generate_dispatch_events(
    trips: list[Trip],
) -> list[DispatchEvent]:

    events = []

    for trip in trips:

        events.append(
            DispatchEvent(
                trip_id=trip.trip_id,
                driver=trip.driver,
                event_type=DispatchEventType.TRIP_ASSIGNED,
                event_time=trip.actual_start,
            )
        )

        events.append(
            DispatchEvent(
                trip_id=trip.trip_id,
                driver=trip.driver,
                event_type=DispatchEventType.TRIP_COMPLETED,
                event_time=trip.actual_end,
            )
        )

    return events