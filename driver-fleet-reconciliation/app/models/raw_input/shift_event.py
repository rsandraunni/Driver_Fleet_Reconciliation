from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.models.base import Base


class ShiftEventType(enum.Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"


class ShiftEvent(Base):
    __tablename__ = "shift_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id"),
        nullable=False
    )

    event_type: Mapped[ShiftEventType] = mapped_column(
        Enum(ShiftEventType),
        nullable=False
    )

    event_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    driver = relationship("Driver")