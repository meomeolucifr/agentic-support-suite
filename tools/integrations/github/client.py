"""GitHub integration client."""
import os
import json
from typing import Dict, Any, Optional, List
import httpx


class GitHubClient:
    """GitHub API client."""
    
    def __init__(self):
        """Initialize GitHub client."""
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_owner = os.getenv("GITHUB_REPO_OWNER")
        self.repo_name = os.getenv("GITHUB_REPO_NAME")
        
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        if not self.repo_owner or not self.repo_name:
            raise ValueError("GITHUB_REPO_OWNER and GITHUB_REPO_NAME are required")
        
        self.base_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create GitHub issue.
        
        Args:
            title: Issue title
            body: Issue body
            labels: Labels to add (optional)
            assignees: Assignees (optional)
            
        Returns:
            Created issue data or None if failed
        """
        payload = {
            "title": title,
            "body": body
        }
        
        if labels:
            payload["labels"] = labels
        if assignees:
            payload["assignees"] = assignees
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/issues",
                    headers=self.headers,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Failed to create GitHub issue: {e}")
                return None
    
    async def update_issue(
        self,
        issue_number: int,
        state: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """Update GitHub issue."""
        payload = {}
        
        if state:
            payload["state"] = state
        if title:
            payload["title"] = title
        if body:
            payload["body"] = body
        if labels:
            payload["labels"] = labels
        
        if not payload:
            return None
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(
                    f"{self.base_url}/issues/{issue_number}",
                    headers=self.headers,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Failed to update GitHub issue: {e}")
                return None
    
    async def create_issue_from_ticket(
        self,
        ticket_id: str,
        ticket_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create GitHub issue from support ticket."""
        title = f"[Support] {ticket_data.get('subject', 'Ticket')} - {ticket_id}"
        
        body = f"""Support Ticket: {ticket_id}

**Category:** {ticket_data.get('category', 'N/A')}
**Priority:** {ticket_data.get('priority', 'N/A')}

**Description:**
{ticket_data.get('body', 'N/A')}

**Context:**
```json
{json.dumps(ticket_data.get('context', {}), indent=2)}
```

This issue was automatically created from a support ticket escalation.
"""
        
        labels = ["support", "ticket"]
        if ticket_data.get("priority") == "HIGH":
            labels.append("priority-high")
        
        return await self.create_issue(
            title=title,
            body=body,
            labels=labels
        )

