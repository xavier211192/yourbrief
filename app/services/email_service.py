"""
Email Service - Send briefs via SendGrid.
"""
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_brief_html(classifications: List[Dict[str, Any]]) -> str:
    """
    Generate HTML content for the brief.

    Args:
        classifications: List of classified email dicts

    Returns:
        HTML string
    """
    # Organize emails by category
    action_items = [c for c in classifications if c['category'] == 'action']
    waiting_items = [c for c in classifications if c['category'] == 'waiting']
    info_items = [c for c in classifications if c['category'] == 'info']
    ignore_items = [c for c in classifications if c['category'] == 'ignore']

    # Sort action items by priority (high -> medium -> low)
    priority_order = {'high': 0, 'medium': 1, 'low': 2, None: 3}
    action_items.sort(key=lambda x: priority_order.get(x.get('priority'), 3))

    # Limit items per section
    max_action = 5
    max_waiting = 3
    max_info = 5

    action_items = action_items[:max_action]
    waiting_items = waiting_items[:max_waiting]
    info_items = info_items[:max_info]

    # Prepare template data
    template_data = {
        'date': datetime.now().strftime('%A, %B %d, %Y'),
        'total_emails': len(classifications),
        'action_count': len([c for c in classifications if c['category'] == 'action']),
        'waiting_count': len([c for c in classifications if c['category'] == 'waiting']),
        'info_count': len([c for c in classifications if c['category'] == 'info']),
        'ignore_count': len(ignore_items),
        'action_items': action_items,
        'waiting_items': waiting_items,
        'info_items': info_items,
        'ignore_items': ignore_items,
    }

    # Set up Jinja2 environment
    template_dir = Path(__file__).parent.parent.parent / 'templates'
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template('brief_email.html')

    # Render template
    html_content = template.render(**template_data)
    return html_content


def send_brief_email(classifications: List[Dict[str, Any]], recipient_email: str = None) -> bool:
    """
    Send brief via SendGrid.

    Args:
        classifications: List of classified email dicts
        recipient_email: Email to send to (defaults to USER_EMAIL from .env)

    Returns:
        True if sent successfully, False otherwise
    """
    print(f"📧 Preparing to send brief via email...")

    # Get SendGrid configuration
    api_key = os.getenv('SENDGRID_API_KEY')
    from_email = os.getenv('SENDGRID_FROM_EMAIL')
    from_name = os.getenv('SENDGRID_FROM_NAME', 'Your Brief')
    to_email = recipient_email or os.getenv('USER_EMAIL')

    # Validate configuration
    if not api_key:
        print("❌ Error: SENDGRID_API_KEY not found in .env file")
        return False

    if not from_email:
        print("❌ Error: SENDGRID_FROM_EMAIL not found in .env file")
        return False

    if not to_email:
        print("❌ Error: Recipient email not provided and USER_EMAIL not set in .env")
        return False

    # Generate subject line
    action_count = len([c for c in classifications if c['category'] == 'action'])
    waiting_count = len([c for c in classifications if c['category'] == 'waiting'])
    date_str = datetime.now().strftime('%b %d')
    subject = f"Your Brief - {date_str}: {action_count} actions, {waiting_count} waiting"

    # Generate HTML content
    html_content = generate_brief_html(classifications)

    # Create plain text version (simplified)
    action_items = [c for c in classifications if c['category'] == 'action']
    plain_text = f"Your Brief - {datetime.now().strftime('%A, %B %d, %Y')}\n\n"
    plain_text += f"You have {action_count} action items requiring attention.\n\n"

    if action_items:
        plain_text += "ACTION REQUIRED:\n"
        for item in action_items[:5]:
            plain_text += f"\n- {item['subject']}\n"
            plain_text += f"  From: {item['sender_name']}\n"
            if item.get('what_needed'):
                plain_text += f"  What: {item['what_needed']}\n"
            if item.get('deadline'):
                plain_text += f"  Deadline: {item['deadline']}\n"

    plain_text += f"\n\nOpen the email in your browser for the full formatted brief."

    try:
        # Create SendGrid message
        message = Mail(
            from_email=Email(from_email, from_name),
            to_emails=To(to_email),
            subject=subject,
            plain_text_content=Content("text/plain", plain_text),
            html_content=Content("text/html", html_content)
        )

        # Send via SendGrid
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        if response.status_code in [200, 201, 202]:
            print(f"✅ Brief sent successfully to {to_email}!")
            print(f"   Status: {response.status_code}")
            return True
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"   Body: {response.body}")
            return False

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


if __name__ == '__main__':
    """Quick test of email service."""
    from app.services.gmail_service import fetch_recent_emails
    from app.services.classifier_service import classify_emails

    # Fetch and classify emails
    print("🔍 Fetching emails...")
    emails = fetch_recent_emails(hours=24)

    if not emails:
        print("No emails to send brief for")
        exit(0)

    print("🤖 Classifying emails...")
    classifications = classify_emails(emails)

    # Send brief
    success = send_brief_email(classifications)

    if success:
        print("\n✨ Done! Check your inbox for the brief.")
    else:
        print("\n⚠️  Failed to send brief. Check the errors above.")
