"""Analytics aggregation utilities."""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from tools.monitoring.metrics import get_metrics_collector


def aggregate_ticket_metrics(time_period_hours: int = 24) -> Dict[str, Any]:
    """
    Aggregate ticket processing metrics.
    
    Args:
        time_period_hours: Time period in hours
        
    Returns:
        Aggregated metrics
    """
    collector = get_metrics_collector()
    metrics = collector.get_metrics()
    
    cutoff_time = datetime.utcnow() - timedelta(hours=time_period_hours)
    
    # Filter recent ticket processing times
    recent_tickets = [
        t for t in metrics.get("ticket_processing_times", [])
        if datetime.fromisoformat(t["timestamp"]) > cutoff_time
    ]
    
    if not recent_tickets:
        return {
            "total_tickets": 0,
            "avg_processing_time": 0,
            "min_processing_time": 0,
            "max_processing_time": 0
        }
    
    durations = [t["duration"] for t in recent_tickets]
    
    return {
        "total_tickets": len(recent_tickets),
        "avg_processing_time": sum(durations) / len(durations),
        "min_processing_time": min(durations),
        "max_processing_time": max(durations),
        "time_period_hours": time_period_hours
    }


def aggregate_agent_metrics(time_period_hours: int = 24) -> Dict[str, Any]:
    """
    Aggregate agent call metrics.
    
    Args:
        time_period_hours: Time period in hours
        
    Returns:
        Aggregated agent metrics
    """
    collector = get_metrics_collector()
    metrics = collector.get_metrics()
    
    cutoff_time = datetime.utcnow() - timedelta(hours=time_period_hours)
    
    # Filter recent agent calls
    recent_calls = [
        c for c in metrics.get("agent_calls", [])
        if datetime.fromisoformat(c["timestamp"]) > cutoff_time
    ]
    
    if not recent_calls:
        return {
            "total_calls": 0,
            "success_rate": 0,
            "avg_duration": 0,
            "by_agent": {}
        }
    
    # Group by agent
    by_agent: Dict[str, List[Dict[str, Any]]] = {}
    for call in recent_calls:
        agent = call["agent"]
        if agent not in by_agent:
            by_agent[agent] = []
        by_agent[agent].append(call)
    
    # Calculate metrics per agent
    agent_metrics = {}
    for agent, calls in by_agent.items():
        success_count = sum(1 for c in calls if c["success"])
        durations = [c["duration"] for c in calls]
        
        agent_metrics[agent] = {
            "total_calls": len(calls),
            "success_count": success_count,
            "success_rate": success_count / len(calls) if calls else 0,
            "avg_duration": sum(durations) / len(durations) if durations else 0
        }
    
    total_success = sum(1 for c in recent_calls if c["success"])
    all_durations = [c["duration"] for c in recent_calls]
    
    return {
        "total_calls": len(recent_calls),
        "success_rate": total_success / len(recent_calls) if recent_calls else 0,
        "avg_duration": sum(all_durations) / len(all_durations) if all_durations else 0,
        "by_agent": agent_metrics
    }



