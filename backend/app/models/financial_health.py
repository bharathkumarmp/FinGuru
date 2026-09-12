from datetime import datetime

from sqlalchemy import DateTime, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FinancialHealth(Base):
    __tablename__ = "financial_health"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    health_level: Mapped[str] = mapped_column(
        nullable=False,
    )

    income_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    spending_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    savings_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    debt_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    stability_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    monthly_income: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    monthly_spending: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    savings_rate: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    emi_ratio: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    balance_volatility: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    weaknesses: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    recommendations: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
