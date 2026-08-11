from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.models.base import Base


class DispatchEventType(enum.Enum):
    TRIP_ASSIGNED = "TRIP_ASSIGNED"
    TRIP_COMPLETED = "TRIP_COMPLETED"


class DispatchEvent(Base):
    __tablename__ = "dispatch_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=False
    )

    event_type: Mapped[DispatchEventType] = mapped_column(
        Enum(DispatchEventType),
        nullable=False
    )

    event_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    driver = relationship("Driver")