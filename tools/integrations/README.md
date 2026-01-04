# Integration Tools

## Purpose

External service integrations for notifications and external system communication (Slack, Email, GitHub).

## Structure

```
integrations/
├── slack/              # Slack webhook integration
│   └── client.py
├── email/              # Email SMTP integration
│   └── client.py
└── github/             # GitHub API integration
    └── client.py
```

## Tech Stack

- **Slack**: Webhook API
- **Email**: SMTP (smtplib)
- **GitHub**: GitHub REST API (httpx)

## Key Components

### Slack Client
- Send notifications to Slack channels
- Format messages for support team
- Include ticket context and links

### Email Client
- Send emails via SMTP
- HTML and plain text support
- Customer-facing email templates

### GitHub Client
- Create issues in GitHub
- Link tickets to GitHub issues
- Update issue status

## Usage Examples

### Slack Notification

```python
from tools.integrations.slack.client import SlackClient

slack = SlackClient()
await slack.send_notification(
    channel="#support",
    message="New ticket escalated",
    context={"ticket_id": "TKT_123", "priority": "HIGH"}
)
```

### Email Customer

```python
from tools.integrations.email.client import EmailClient

email = EmailClient()
await email.send_email(
    to="customer@example.com",
    subject="Your ticket has been resolved",
    body="We've processed your refund..."
)
```

### Create GitHub Issue

```python
from tools.integrations.github.client import GitHubClient

github = GitHubClient()
issue = await github.create_issue(
    title="Bug: Duplicate charge issue",
    body="Customer reported duplicate charge...",
    labels=["bug", "billing"]
)
```

## Configuration

- `SLACK_WEBHOOK_URL` - Slack webhook URL
- `EMAIL_SMTP_HOST`, `EMAIL_SMTP_PORT`, `EMAIL_SMTP_USER`, `EMAIL_SMTP_PASSWORD`
- `GITHUB_TOKEN`, `GITHUB_REPO_OWNER`, `GITHUB_REPO_NAME`



