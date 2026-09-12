from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.events.event_types import EventType
from app.events.publisher import create_event, publish_event
from app.events.consumer import process_event


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class EventCreateRequest(BaseModel):
    event_type: str = Field(
        ...,
        description="Type of banking event"
    )

    customer_id: int = Field(
        ...,
        gt=0
    )

    transaction_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    data: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# EVENT SERIALIZER
# ============================================================

def event_to_dict(event: Any) -> dict:
    """
    Convert an event object/dictionary into a JSON-safe dict.
    """

    if isinstance(event, dict):
        return event

    if hasattr(event, "model_dump"):
        return event.model_dump()

    if hasattr(event, "dict"):
        return event.dict()

    if hasattr(event, "__dict__"):
        return {
            key: value
            for key, value in vars(event).items()
            if not key.startswith("_")
        }

    return {
        "event": str(event)
    }


# ============================================================
# GET EVENT TYPES
# ============================================================

@router.get("/types")
def get_event_types():
    """
    Return all supported FinGuru event types.
    """

    return {
        "success": True,
        "event_types": [
            event.value
            for event in EventType
        ],
    }


# ============================================================
# CREATE AND PROCESS EVENT
# ============================================================

@router.post("")
def create_and_process_event(
    request: EventCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Create, publish and process a banking event.

    Flow:

    API Request
        ↓
    Event Creation
        ↓
    Event Publisher
        ↓
    Event Consumer
        ↓
    Event Handler
    """

    # --------------------------------------------------------
    # VALIDATE EVENT TYPE
    # --------------------------------------------------------

    try:

        event_type = EventType(
            request.event_type
        )

    except ValueError:

        valid_types = [
            event.value
            for event in EventType
        ]

        raise HTTPException(
            status_code=400,
            detail={
                "message": (
                    f"Unsupported event type: "
                    f"{request.event_type}"
                ),
                "valid_event_types": valid_types,
            },
        )

    # --------------------------------------------------------
    # CREATE EVENT
    # --------------------------------------------------------

    try:

        event = create_event(
            event_type=event_type,
            customer_id=request.customer_id,
            transaction_id=request.transaction_id,
            data=request.data,
        )

    except TypeError:

        # Compatibility fallback for event
        # implementations that use a different
        # argument structure.

        try:

            event = create_event(
                event_type=event_type,
                customer_id=request.customer_id,
                data=request.data,
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Event creation failed: "
                    f"{exc}"
                ),
            )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Event creation failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # PUBLISH EVENT
    # --------------------------------------------------------

    try:

        published = publish_event(
            event
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Event publishing failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # PROCESS EVENT
    # --------------------------------------------------------

    try:

        processed = process_event(
            event,
            db=db,
        )

    except TypeError:

        # Compatibility fallback if the consumer
        # does not require the database argument.

        try:

            processed = process_event(
                event
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Event processing failed: "
                    f"{exc}"
                ),
            )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Event processing failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,
        "message": "Event created and processed",
        "event_type": event_type.value,
        "customer_id": request.customer_id,
        "transaction_id": request.transaction_id,
        "published": published,
        "processed": processed,
        "event": event_to_dict(event),
    }


# ============================================================
# PUBLISH EVENT ONLY
# ============================================================

@router.post("/publish")
def publish_event_only(
    request: EventCreateRequest,
):
    """
    Create and publish an event without processing it
    immediately.
    """

    # --------------------------------------------------------
    # VALIDATE EVENT TYPE
    # --------------------------------------------------------

    try:

        event_type = EventType(
            request.event_type
        )

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail={
                "message": (
                    f"Unsupported event type: "
                    f"{request.event_type}"
                ),
                "valid_event_types": [
                    event.value
                    for event in EventType
                ],
            },
        )

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------

    try:

        event = create_event(
            event_type=event_type,
            customer_id=request.customer_id,
            transaction_id=request.transaction_id,
            data=request.data,
        )

    except TypeError:

        try:

            event = create_event(
                event_type=event_type,
                customer_id=request.customer_id,
                data=request.data,
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Event creation failed: "
                    f"{exc}"
                ),
            )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Event creation failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # PUBLISH
    # --------------------------------------------------------

    try:

        published = publish_event(
            event
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Event publishing failed: "
                f"{exc}"
            ),
        )

    return {
        "success": True,
        "message": "Event published successfully",
        "event_type": event_type.value,
        "customer_id": request.customer_id,
        "transaction_id": request.transaction_id,
        "published": published,
        "event": event_to_dict(event),
    }


# ============================================================
# PROCESS EVENT
# ============================================================

@router.post("/process")
def process_existing_event(
    event: dict[str, Any],
    db: Session = Depends(get_db),
):
    """
    Process an already-created event.
    """

    if not event:

        raise HTTPException(
            status_code=400,
            detail="Event payload cannot be empty",
        )

    try:

        result = process_event(
            event,
            db=db,
        )

    except TypeError:

        try:

            result = process_event(
                event
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Event processing failed: "
                    f"{exc}"
                ),
            )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Event processing failed: "
                f"{exc}"
            ),
        )

    return {
        "success": True,
        "message": "Event processed successfully",
        "result": result,
    }