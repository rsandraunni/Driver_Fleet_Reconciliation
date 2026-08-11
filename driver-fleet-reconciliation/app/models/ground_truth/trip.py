from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=False
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=False
    )

    trip_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    planned_start: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    planned_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    actual_start: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    actual_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    distance_km: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    driver = relationship(
        "Driver",
        back_populates="trips"
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="trips"
    )