"""Slack integration client."""
import os
import json
from typing import Dict, Any, Optional
import httpx


class SlackClient:
    """Slack webhook client."""
    
    def __init__(self):
        """Initialize Slack client."""
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError("SLACK_WEBHOOK_URL environment variable is required")
    
    async def send_notification(
        self,
        message: str,
        channel: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        priority: str = "MEDIUM"
    ) -> bool:
        """
        Send notification to Slack.
        
        Args:
            message: Main message
            channel: Channel name (optional, uses webhook default)
            context: Additional context data
            priority: Priority level (LOW, MEDIUM, HIGH, URGENT)
            
        Returns:
            True if successful
        """
        # Color based on priority
        color_map = {
            "LOW": "#36a64f",      # Green
            "MEDIUM": "#ffa500",   # Orange
            "HIGH": "#ff0000",     # Red
            "URGENT": "#8b0000"    # Dark red
        }
        color = color_map.get(priority, "#36a64f")
        
        # Build Slack message
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"Support Ticket Alert ({priority})"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
        
        # Add context if provided
        if context:
            context_text = "\n".join([
                f"*{k}:* {v}" for k, v in context.items()
            ])
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Context:*\n{context_text}"
                }
            })
        
        payload = {
            "blocks": blocks,
            "attachments": [
                {
                    "color": color,
                    "footer": "Customer Support System"
                }
            ]
        }
        
        if channel:
            payload["channel"] = channel
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return True
            except Exception as e:
                print(f"Failed to send Slack notification: {e}")
                return False
    
    async def send_ticket_escalation(
        self,
        ticket_id: str,
        priority: str,
        context: Dict[str, Any]
    ) -> bool:
        """Send ticket escalation notification."""
        message = f"🚨 Ticket {ticket_id} requires attention"
        return await self.send_notification(
            message=message,
            context=context,
            priority=priority
        )



