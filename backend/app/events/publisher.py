from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from app.events.event_types import EventType


def create_event(
    event_type: EventType | str,
    customer_id: int,
    data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Create a standardized FinGuru event.
    """

    if isinstance(event_type, EventType):
        event_name = event_type.value
    else:
        event_name = str(event_type)

    return {
        "event_id": str(uuid4()),
        "event_type": event_name,
        "customer_id": customer_id,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data or {},
    }


def publish_event(
    event_type: EventType | str,
    customer_id: int,
    data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Publish an event.

    For the prototype, events are returned as
    standardized dictionaries.

    Redis Streams can be connected through
    redis_stream.py without changing the
    event format.
    """

    event = create_event(
        event_type=event_type,
        customer_id=customer_id,
        data=data,
    )

    return event