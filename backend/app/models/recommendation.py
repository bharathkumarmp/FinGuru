from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    need_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    affordability_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    suitability_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    timing_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    preference_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    financial_health_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    reasons: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
