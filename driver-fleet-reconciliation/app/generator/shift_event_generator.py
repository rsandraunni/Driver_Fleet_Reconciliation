import random
from datetime import timedelta

from app.models.ground_truth.shift import Shift
from app.models.raw_input.shift_event import (
    ShiftEvent,
    ShiftEventType,
)


def generate_shift_events(
    shifts: list[Shift],
) -> list[ShiftEvent]:

    events = []

    for shift in shifts:

        login = shift.login_time + timedelta(
            minutes=random.randint(-3, 3)
        )

        logout = shift.logout_time + timedelta(
            minutes=random.randint(-3, 3)
        )

        events.append(
            ShiftEvent(
                driver=shift.driver,
                event_type=ShiftEventType.LOGIN,
                event_time=login,
            )
        )

        events.append(
            ShiftEvent(
                driver=shift.driver,
                event_type=ShiftEventType.LOGOUT,
                event_time=logout,
            )
        )

    return events