"""
Classifier Service - Classify emails using OpenAI.
"""
import os
import json
from typing import List, Dict, Any

from openai import OpenAI
from dotenv import load_dotenv

from app.prompts.classification_prompt import SYSTEM_PROMPT, build_classification_prompt

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def classify_emails(emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Classify a list of emails using OpenAI.

    Args:
        emails: List of email dicts from Gmail service

    Returns:
        List of classification dicts with keys:
            - email_index: Index in original list
            - gmail_id: Gmail message ID
            - category: action/waiting/info/ignore
            - priority: high/medium/low or null
            - what_needed: Description or null
            - deadline: Deadline text or null
            - sender_name: From original email
            - sender_email: From original email
            - subject: From original email
    """
    if not emails:
        print("⚠️  No emails to classify")
        return []

    print(f"🤖 Classifying {len(emails)} emails with AI...")

    # Build the prompt
    user_prompt = build_classification_prompt(emails)

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent classifications
            response_format={"type": "json_object"}
        )

        # Extract the response
        content = response.choices[0].message.content

        # Parse JSON response
        classifications_raw = json.loads(content)

        # Handle if response is wrapped in a key (e.g., {"classifications": [...]})
        if isinstance(classifications_raw, dict):
            # Try common keys
            for key in ['classifications', 'results', 'emails', 'data']:
                if key in classifications_raw:
                    classifications_raw = classifications_raw[key]
                    break

            # If still a dict, check if all values are dicts (might be indexed by number)
            if isinstance(classifications_raw, dict):
                # Check if keys are numeric strings
                if all(k.isdigit() for k in classifications_raw.keys()):
                    # Convert to list sorted by key
                    classifications_raw = [classifications_raw[str(i)] for i in range(len(classifications_raw))]
                else:
                    # Just take all values if they look like classification objects
                    values = list(classifications_raw.values())
                    if values and isinstance(values[0], dict) and 'category' in values[0]:
                        classifications_raw = values

        # Ensure we have a list
        if not isinstance(classifications_raw, list):
            print(f"⚠️  Unexpected response format. Got: {type(classifications_raw)}")
            print(f"Content preview: {str(classifications_raw)[:500]}")
            raise ValueError(f"Expected array of classifications, got {type(classifications_raw)}")

        # Merge classifications with original email data
        classifications = []
        for i, (email, classification) in enumerate(zip(emails, classifications_raw)):
            classifications.append({
                'email_index': i,
                'gmail_id': email['gmail_id'],
                'thread_id': email['thread_id'],
                'sender_name': email['sender_name'],
                'sender_email': email['sender_email'],
                'subject': email['subject'],
                'snippet': email['snippet'],
                'received_date': email['received_date'],
                'category': classification.get('category'),
                'priority': classification.get('priority'),
                'what_needed': classification.get('what_needed'),
                'deadline': classification.get('deadline'),
            })

        print(f"✅ Classified {len(classifications)} emails successfully")

        # Print token usage for transparency
        print(f"💰 Tokens used - Input: {response.usage.prompt_tokens}, Output: {response.usage.completion_tokens}")

        return classifications

    except Exception as e:
        print(f"❌ Error classifying emails: {e}")
        raise


def print_classification_summary(classifications: List[Dict[str, Any]]):
    """
    Print a nice summary of classifications.

    Args:
        classifications: List of classification dicts
    """
    # Count by category
    counts = {
        'action': 0,
        'waiting': 0,
        'info': 0,
        'ignore': 0
    }

    for c in classifications:
        category = c.get('category', 'unknown')
        if category in counts:
            counts[category] += 1

    print("\n📊 Classification Summary:")
    print(f"🔴 Action Required: {counts['action']}")
    print(f"🟡 Waiting On Others: {counts['waiting']}")
    print(f"🟢 Info Only: {counts['info']}")
    print(f"⚪ Ignore/Noise: {counts['ignore']}")

    # Show action items
    action_items = [c for c in classifications if c['category'] == 'action']
    if action_items:
        print("\n🔴 ACTION REQUIRED EMAILS:")
        for item in action_items:
            priority_emoji = "🔥" if item['priority'] == 'high' else "📌" if item['priority'] == 'medium' else "📍"
            print(f"\n  {priority_emoji} From: {item['sender_name']}")
            print(f"     Subject: {item['subject']}")
            if item['what_needed']:
                print(f"     What: {item['what_needed']}")
            if item['deadline']:
                print(f"     Deadline: {item['deadline']}")


if __name__ == '__main__':
    """Quick test of classifier service."""
    from app.services.gmail_service import fetch_recent_emails

    # Fetch emails
    emails = fetch_recent_emails(hours=24)

    if not emails:
        print("No emails to classify")
        exit(0)

    # Classify them
    classifications = classify_emails(emails)

    # Print summary
    print_classification_summary(classifications)

    # Show a few examples
    print("\n📧 Sample Classifications (first 3):")
    for c in classifications[:3]:
        print(f"\nFrom: {c['sender_name']}")
        print(f"Subject: {c['subject']}")
        print(f"Category: {c['category']}")
        if c['category'] in ['action', 'waiting']:
            print(f"Priority: {c['priority']}")
            print(f"What needed: {c['what_needed']}")
            print(f"Deadline: {c['deadline']}")
