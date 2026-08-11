from datetime import date
import enum

#from sqlalchemy import Date, Enum, Float, Integer, String, UniqueConstraint
from sqlalchemy import (
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)


from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class SummaryStatus(enum.Enum):
    RESOLVED = "RESOLVED"
    RESOLVED_WITH_FLAGS = "RESOLVED_WITH_FLAGS"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class DailySummary(Base):
    __tablename__ = "daily_summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    '''
    driver_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    '''
    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=False
    )

    driver = relationship("Driver")
    




    summary_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    hours_on_duty: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    trips_completed: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    distance_km: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    status: Mapped[SummaryStatus] = mapped_column(
        Enum(SummaryStatus),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "driver_id",
            "summary_date",
            name="uq_driver_summary_date"
        ),
    )