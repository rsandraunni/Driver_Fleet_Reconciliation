from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(primary_key=True)

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=False
    )

    shift_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    login_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    logout_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    driver = relationship(
        "Driver",
        back_populates="shifts"
    )