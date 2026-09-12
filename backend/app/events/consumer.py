from typing import Any, Dict, List

from app.events.handlers import handle_event
from app.events.redis_stream import event_stream


def process_event(
    event: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Process one FinGuru event.
    """

    return handle_event(event)


def process_events(
    events: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Process multiple events.
    """

    results = []

    for event in events:

        result = process_event(event)

        results.append(result)

    return results


def consume_from_redis(
    count: int = 10,
    block: int = 1000,
):
    """
    Consume events from Redis Stream.

    This is optional for the prototype.
    """

    messages = event_stream.read(
        count=count,
        block=block,
    )

    processed = []

    for stream_name, entries in messages:

        for message_id, values in entries:

            processed.append({
                "message_id": message_id,
                "stream": stream_name,
                "values": values,
            })

    return processed