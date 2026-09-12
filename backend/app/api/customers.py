from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.customer_360 import get_customer_360


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get("/{customer_id}")
def customer_360(
    customer_id: int,
    db: Session = Depends(get_db),
):
    try:
        data = get_customer_360(
            db=db,
            customer_id=customer_id,
        )

        return {
            "success": True,
            "data": data,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Customer 360 failed: {exc}",
        )
