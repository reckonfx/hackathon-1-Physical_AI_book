from typing import Dict, Any, Callable
from datetime import datetime
from backend.utils.logger import TranslationLogger


class RateLimitNotifier:
    """
    System for notifying users about API rate limiting.
    """

    def __init__(self):
        self.logger = TranslationLogger("rate_limit")
        self.notifiers: Dict[str, Callable] = {}

    def register_notifier(self, name: str, notifier_func: Callable):
        """Register a custom notifier function."""
        self.notifiers[name] = notifier_func

    def notify_rate_limit_exceeded(
        self,
        client_id: str,
        limit: int,
        window: int,
        current_count: int = None
    ):
        """
        Notify that rate limit has been exceeded for a client.

        Args:
            client_id: Identifier for the client (e.g., IP address)
            limit: Maximum requests allowed
            window: Time window in seconds
            current_count: Current request count (optional)
        """
        message = (
            f"Rate limit exceeded for client {client_id}. "
            f"Limit: {limit} requests per {window}s."
        )
        if current_count:
            message += f" Current count: {current_count}."

        # Log the event
        self.logger.log_rate_limit_event(client_id, limit, window)

        # Execute registered notifiers
        for name, notifier in self.notifiers.items():
            try:
                notifier(client_id, limit, window, current_count)
            except Exception as e:
                # Log notifier errors but don't fail the main operation
                self.logger.log_error("NOTIFIER_ERROR", f"Notifier {name} failed: {str(e)}")

    def notify_approaching_limit(
        self,
        client_id: str,
        limit: int,
        current_count: int,
        threshold: float = 0.8
    ):
        """
        Notify when a client is approaching their rate limit.

        Args:
            client_id: Identifier for the client
            limit: Maximum requests allowed
            current_count: Current request count
            threshold: Threshold percentage (0.8 = 80%)
        """
        if current_count >= limit * threshold:
            message = (
                f"Client {client_id} approaching rate limit. "
                f"Used {current_count}/{limit} requests."
            )

            # Log the event
            self.logger.log_error("RATE_LIMIT_APPROACHING", message, {
                "client_id": client_id,
                "current_count": current_count,
                "limit": limit,
                "threshold": threshold
            })

            # Execute registered notifiers
            for name, notifier in self.notifiers.items():
                try:
                    # Use a different notification for approaching limit
                    notifier(f"approaching_{client_id}", limit, 3600, current_count)
                except Exception as e:
                    self.logger.log_error("NOTIFIER_ERROR", f"Notifier {name} failed: {str(e)}")


# Global rate limit notifier instance
rate_limit_notifier = RateLimitNotifier()