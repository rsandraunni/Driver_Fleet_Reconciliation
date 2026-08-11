from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    registration_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    assignments = relationship(
        "Assignment",
        back_populates="vehicle"
    )

    trips = relationship(
        "Trip",
        back_populates="vehicle"
    )