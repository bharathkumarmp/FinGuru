from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FinancialStress(Base):
    __tablename__ = "financial_stress"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    stress_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    stress_level: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    income_change: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    spending_change: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    balance_change: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    emi_ratio: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    missed_emi_count: Mapped[int] = mapped_column(
        default=0,
    )

    savings_rate: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    cash_buffer: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
