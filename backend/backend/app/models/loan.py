from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    loan_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    principal_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    interest_rate: Mapped[float] = mapped_column(
        nullable=False,
    )

    tenure_months: Mapped[int] = mapped_column(
        nullable=False,
    )

    monthly_emi: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    outstanding_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )