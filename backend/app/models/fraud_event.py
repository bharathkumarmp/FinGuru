from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FraudEvent(Base):
    __tablename__ = "fraud_events"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    transaction_id: Mapped[int | None] = mapped_column(
        nullable=True,
        index=True,
    )

    fraud_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    anomaly_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    rule_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    identity_risk_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    recommended_action: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
