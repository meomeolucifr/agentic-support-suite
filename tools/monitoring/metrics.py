"""Metrics collection utilities."""
from typing import Dict, Any
from datetime import datetime
import time


class MetricsCollector:
    """Simple metrics collector."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.metrics: Dict[str, Any] = {}
    
    def record_ticket_processing_time(self, ticket_id: str, duration: float):
        """Record ticket processing time."""
        if "ticket_processing_times" not in self.metrics:
            self.metrics["ticket_processing_times"] = []
        
        self.metrics["ticket_processing_times"].append({
            "ticket_id": ticket_id,
            "duration": duration,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def record_agent_call(self, agent_name: str, success: bool, duration: float):
        """Record agent call metrics."""
        if "agent_calls" not in self.metrics:
            self.metrics["agent_calls"] = []
        
        self.metrics["agent_calls"].append({
            "agent": agent_name,
            "success": success,
            "duration": duration,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        return self.metrics
    
    def reset(self):
        """Reset metrics."""
        self.metrics = {}


# Global metrics collector
_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector."""
    return _metrics_collector



