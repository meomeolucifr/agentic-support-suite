"""Email integration client."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from typing import Dict, Any


class EmailClient:
    """SMTP email client."""
    
    def __init__(self):
        """Initialize email client."""
        self.smtp_host = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
        self.smtp_user = os.getenv("EMAIL_SMTP_USER")
        self.smtp_password = os.getenv("EMAIL_SMTP_PASSWORD")
        self.from_email = os.getenv("EMAIL_FROM", self.smtp_user)
        
        if not self.smtp_user or not self.smtp_password:
            raise ValueError("EMAIL_SMTP_USER and EMAIL_SMTP_PASSWORD are required")
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        cc: Optional[List[str]] = None
    ) -> bool:
        """
        Send email.
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Plain text body
            html_body: HTML body (optional)
            cc: CC recipients (optional)
            
        Returns:
            True if successful
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = self.from_email
        msg["To"] = to
        msg["Subject"] = subject
        
        if cc:
            msg["Cc"] = ", ".join(cc)
        
        # Add plain text part
        msg.attach(MIMEText(body, "plain"))
        
        # Add HTML part if provided
        if html_body:
            msg.attach(MIMEText(html_body, "html"))
        
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                recipients = [to]
                if cc:
                    recipients.extend(cc)
                server.send_message(msg, to_addrs=recipients)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    async def send_ticket_response(
        self,
        customer_email: str,
        ticket_id: str,
        message: str,
        is_resolved: bool = False
    ) -> bool:
        """Send ticket response email to customer."""
        subject = f"Re: Your Support Ticket {ticket_id}"
        
        if is_resolved:
            body = f"""Hello,

Your support ticket {ticket_id} has been resolved.

{message}

If you have any further questions, please don't hesitate to reach out.

Best regards,
Support Team"""
        else:
            body = f"""Hello,

Thank you for contacting us. We've received your ticket {ticket_id} and our team is looking into it.

{message}

We'll update you as soon as we have more information.

Best regards,
Support Team"""
        
        return await self.send_email(
            to=customer_email,
            subject=subject,
            body=body
        )



