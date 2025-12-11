import time
from typing import Dict
from fastapi import Request, HTTPException
from backend.config import RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW


class RateLimiter:
    """
    Simple in-memory rate limiter.
    In production, consider using Redis or other distributed storage.
    """
    def __init__(self):
        self.requests: Dict[str, list] = {}  # IP -> list of request timestamps
        self.limit = RATE_LIMIT_REQUESTS
        self.window = RATE_LIMIT_WINDOW

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.

        Args:
            identifier: Unique identifier (e.g., IP address)

        Returns:
            True if request is allowed, False otherwise
        """
        current_time = time.time()

        # Clean old requests outside the time window
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if current_time - req_time < self.window
            ]
        else:
            self.requests[identifier] = []

        # Check if limit is exceeded
        if len(self.requests[identifier]) >= self.limit:
            return False

        # Add current request
        self.requests[identifier].append(current_time)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit_middleware(request: Request) -> None:
    """
    Rate limiting middleware function.
    """
    # Use client IP as identifier (consider using X-Forwarded-For in production)
    client_ip = request.client.host

    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )