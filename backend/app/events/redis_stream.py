import json
import os
from typing import Any, Dict, Optional


class RedisEventStream:
    """
    Redis Streams adapter for FinGuru.

    Redis is optional for the prototype.
    The application can still operate without
    a running Redis server.
    """

    def __init__(
        self,
        stream_name: str = "finguru_events",
        redis_url: Optional[str] = None,
    ):
        self.stream_name = stream_name

        self.redis_url = redis_url or os.getenv(
            "REDIS_URL",
            "redis://localhost:6379/0",
        )

        self.client = None

        try:
            import redis

            self.client = redis.Redis.from_url(
                self.redis_url,
                decode_responses=True,
            )

            self.client.ping()

        except Exception:
            self.client = None

    # ========================================================
    # PUBLISH
    # ========================================================

    def publish(
        self,
        event: Dict[str, Any],
    ) -> Optional[str]:
        """
        Publish an event to Redis Stream.

        Returns Redis message ID if Redis is available.
        """

        if self.client is None:
            return None

        message_id = self.client.xadd(
            self.stream_name,
            {
                "event": json.dumps(
                    event,
                    default=str,
                )
            },
        )

        return message_id

    # ========================================================
    # READ
    # ========================================================

    def read(
        self,
        count: int = 10,
        block: int = 1000,
    ):
        """
        Read events from the Redis Stream.
        """

        if self.client is None:
            return []

        return self.client.xread(
            {
                self.stream_name: "0-0"
            },
            count=count,
            block=block,
        )


# Default stream instance
event_stream = RedisEventStream()