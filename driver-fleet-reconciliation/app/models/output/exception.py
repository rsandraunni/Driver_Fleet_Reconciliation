from datetime import date
import enum

from sqlalchemy import Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ExceptionSeverity(enum.Enum):
    BLOCKING = "BLOCKING"
    INFORMATIONAL = "INFORMATIONAL"


class ReconciliationException(Base):
    __tablename__ = "exceptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    summary_id: Mapped[int] = mapped_column(
        ForeignKey("daily_summaries.id"),
        nullable=False
    )

    driver_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    exception_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    reason_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    severity: Mapped[ExceptionSeverity] = mapped_column(
        Enum(ExceptionSeverity),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    summary = relationship("DailySummary")