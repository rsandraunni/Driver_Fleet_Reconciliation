from faker import Faker

from app.models.ground_truth.vehicle import Vehicle

fake = Faker()


def generate_vehicles(count: int = 20) -> list[Vehicle]:
    """
    Generate synthetic vehicle records.
    """

    vehicles = []

    for i in range(1, count + 1):
        vehicle = Vehicle(
            vehicle_id=f"VEH{i:04d}",
            registration_number=fake.unique.license_plate(),
        )

        vehicles.append(vehicle)

    return vehicles