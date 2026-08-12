from faker import Faker

from app.models.ground_truth.driver import Driver

fake = Faker()


def generate_drivers(count: int = 20) -> list[Driver]:
    """
    Generate synthetic driver records.
    """

    drivers = []

    for i in range(1, count + 1):
        driver = Driver(
            driver_id=f"DRV{i:04d}",
            name=fake.name(),
        )

        drivers.append(driver)

    return drivers