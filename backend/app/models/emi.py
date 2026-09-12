from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EMIRecord(Base):
    __tablename__ = "emi_records"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    loan_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    paid_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=Decimal("0"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
