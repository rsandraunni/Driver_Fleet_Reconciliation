from datetime import date

from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True)

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=False
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=False
    )

    assignment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    driver = relationship(
        "Driver",
        back_populates="assignments"
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="assignments"
    )

    __table_args__ = (
        UniqueConstraint(
            "driver_id",
            "assignment_date",
            name="uq_driver_assignment_date"
        ),
    )