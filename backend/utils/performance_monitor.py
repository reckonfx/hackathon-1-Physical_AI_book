import time
import statistics
from typing import Dict, List, Optional
from collections import defaultdict, deque
from datetime import datetime, timedelta


class PerformanceMonitor:
    """
    Performance monitoring for translation response times.
    """

    def __init__(self, max_samples: int = 1000):
        self.max_samples = max_samples
        self.response_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=self.max_samples))
        self.start_times: Dict[str, float] = {}

    def start_timer(self, request_id: str, endpoint: str = "unknown"):
        """Start timing for a request."""
        self.start_times[request_id] = time.time()

    def end_timer(self, request_id: str, endpoint: str = "unknown"):
        """End timing for a request and record the response time."""
        if request_id in self.start_times:
            elapsed = (time.time() - self.start_times[request_id]) * 1000  # Convert to milliseconds
            self.response_times[endpoint].append(elapsed)
            del self.start_times[request_id]
            return elapsed
        return None

    def get_stats(self, endpoint: str = "all") -> Dict[str, float]:
        """Get performance statistics for an endpoint or all endpoints."""
        if endpoint == "all":
            all_times = []
            for times in self.response_times.values():
                all_times.extend(times)
            if not all_times:
                return {"avg": 0, "p95": 0, "p99": 0, "min": 0, "max": 0, "count": 0}

            sorted_times = sorted(all_times)
            return {
                "avg": statistics.mean(all_times),
                "p95": self._percentile(sorted_times, 95),
                "p99": self._percentile(sorted_times, 99),
                "min": min(all_times),
                "max": max(all_times),
                "count": len(all_times)
            }
        else:
            times = list(self.response_times[endpoint])
            if not times:
                return {"avg": 0, "p95": 0, "p99": 0, "min": 0, "max": 0, "count": 0}

            sorted_times = sorted(times)
            return {
                "avg": statistics.mean(times),
                "p95": self._percentile(sorted_times, 95),
                "p99": self._percentile(sorted_times, 99),
                "min": min(times),
                "max": max(times),
                "count": len(times)
            }

    def _percentile(self, sorted_list: List[float], percentile: float) -> float:
        """Calculate percentile of a sorted list."""
        if not sorted_list:
            return 0

        index = (percentile / 100) * (len(sorted_list) - 1)
        lower = int(index)
        upper = min(lower + 1, len(sorted_list) - 1)

        if lower == upper:
            return sorted_list[lower]

        # Interpolate between values
        weight = index - lower
        return sorted_list[lower] * (1 - weight) + sorted_list[upper] * weight

    def get_endpoint_stats(self) -> Dict[str, Dict[str, float]]:
        """Get performance statistics for all endpoints."""
        stats = {}
        for endpoint in self.response_times.keys():
            stats[endpoint] = self.get_stats(endpoint)
        return stats


# Global performance monitor instance
performance_monitor = PerformanceMonitor()