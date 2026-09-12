from datetime import datetime

from sqlalchemy import DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CustomerFeatures(Base):
    __tablename__ = "customer_features"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
        index=True,
    )

    # ========================================================
    # INCOME & SPENDING
    # ========================================================

    avg_monthly_income: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    avg_monthly_spending: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    # ========================================================
    # SAVINGS
    # ========================================================

    savings_rate: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    cash_buffer: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    # ========================================================
    # DEBT / CREDIT
    # ========================================================

    emi_ratio: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    credit_utilization: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    missed_emi_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ========================================================
    # BEHAVIOR
    # ========================================================

    transaction_frequency: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    spending_growth: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    balance_volatility: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    income_stability: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    # ========================================================
    # TIMESTAMP
    # ========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )