"""
Gmail Service - Fetch emails from Gmail API.
"""
import os
import pickle
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scopes - read-only access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    """
    Authenticate with Gmail API using OAuth 2.0.

    Returns:
        Gmail API service object

    Note:
        - First run will open browser for OAuth consent
        - Token saved to token.pickle for subsequent runs
    """
    creds = None
    token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.pickle')
    credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')

    # Load existing token if available
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    # Build and return Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service


def fetch_recent_emails(hours: int = 24) -> List[Dict[str, Any]]:
    """
    Fetch emails from the last N hours.

    Args:
        hours: Number of hours to look back (default: 24)

    Returns:
        List of email dictionaries with keys:
            - gmail_id: Gmail message ID
            - thread_id: Gmail thread ID
            - sender_name: Sender name
            - sender_email: Sender email
            - subject: Email subject
            - snippet: Preview text (~200 chars)
            - received_date: DateTime when received
            - labels: List of Gmail labels
    """
    print(f"🔍 Fetching emails from last {hours} hours...")

    service = authenticate_gmail()

    # Calculate timestamp for N hours ago
    time_ago = datetime.now(timezone.utc) - timedelta(hours=hours)
    query_timestamp = int(time_ago.timestamp())

    # Get SendGrid sender email to exclude from results (avoid analyzing our own briefs)
    sendgrid_from = os.getenv('SENDGRID_FROM_EMAIL', '')

    # Query: emails after timestamp, exclude our own briefs
    query = f'after:{query_timestamp}'
    if sendgrid_from:
        query += f' -from:{sendgrid_from}'

    # Fetch message IDs
    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=100  # Adjust as needed
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("📭 No emails found in the specified time range.")
        return []

    print(f"📬 Found {len(messages)} emails. Fetching details...")

    emails = []
    for msg in messages:
        # Fetch full message details
        message = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        # Parse email data
        email_data = parse_email_message(message)
        emails.append(email_data)

    print(f"✅ Fetched {len(emails)} emails successfully.")
    return emails


def parse_email_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse Gmail API message object into simplified email dict.

    Args:
        message: Gmail API message object

    Returns:
        Simplified email dictionary
    """
    headers = message['payload']['headers']

    # Helper to get header value
    def get_header(name: str) -> str:
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''

    # Parse sender (format: "Name <email@example.com>")
    sender_raw = get_header('From')
    sender_email = sender_raw
    sender_name = sender_raw

    if '<' in sender_raw and '>' in sender_raw:
        sender_name = sender_raw.split('<')[0].strip().strip('"')
        sender_email = sender_raw.split('<')[1].split('>')[0].strip()

    # Parse received date
    internal_date = int(message['internalDate']) / 1000  # Convert from milliseconds
    received_date = datetime.fromtimestamp(internal_date, tz=timezone.utc)

    return {
        'gmail_id': message['id'],
        'thread_id': message['threadId'],
        'sender_name': sender_name,
        'sender_email': sender_email,
        'subject': get_header('Subject'),
        'snippet': message.get('snippet', ''),
        'received_date': received_date,
        'labels': message.get('labelIds', []),
    }


if __name__ == '__main__':
    """Quick test of Gmail service."""
    emails = fetch_recent_emails(hours=24)

    print(f"\n📊 Summary:")
    print(f"Total emails: {len(emails)}")

    if emails:
        print(f"\n📧 Sample (first 3):")
        for email in emails[:3]:
            print(f"\nFrom: {email['sender_name']} <{email['sender_email']}>")
            print(f"Subject: {email['subject']}")
            print(f"Snippet: {email['snippet'][:100]}...")
            print(f"Received: {email['received_date']}")
