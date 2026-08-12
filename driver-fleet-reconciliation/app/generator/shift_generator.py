from datetime import datetime, timedelta, time
import random

from app.models.ground_truth.shift import Shift
from app.models.ground_truth.driver import Driver


def generate_shifts(
    drivers: list[Driver],
    start_date,
    num_days: int,
) -> list[Shift]:

    shifts = []

    for day in range(num_days):

        current_date = start_date + timedelta(days=day)

        for driver in drivers:

            login_hour = random.randint(6, 9)

            login_time = datetime.combine(
                current_date,
                time(login_hour, 0)
            )

            shift_duration = random.randint(8, 10)

            logout_time = login_time + timedelta(
                hours=shift_duration
            )

            shifts.append(
                Shift(
                    driver=driver,
                    shift_date=current_date,
                    login_time=login_time,
                    logout_time=logout_time,
                )
            )

    return shifts