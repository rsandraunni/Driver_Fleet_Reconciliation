from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    assignments = relationship(
        "Assignment",
        back_populates="driver"
    )

    shifts = relationship(
        "Shift",
        back_populates="driver"
    )

    trips = relationship(
        "Trip",
        back_populates="driver"
    )