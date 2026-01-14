#!/usr/bin/env python3
"""
Your Brief - Main Script

Fetches emails from Gmail, classifies them with AI, and generates a daily brief.

Usage:
    python main.py              # Save to HTML file (default)
    python main.py --email      # Send via email
    or
    uv run python main.py
    uv run python main.py --email
"""
import sys
import argparse
from datetime import datetime

from app.services.gmail_service import fetch_recent_emails
from app.services.classifier_service import classify_emails
from app.services.brief_generator import generate_brief
from app.services.email_service import send_brief_email


def main():
    """Main function to generate Your Brief."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate Your Brief - AI-powered email summary')
    parser.add_argument('--email', action='store_true', help='Send brief via email (default: save to HTML)')
    args = parser.parse_args()

    print("=" * 60)
    print("☀️  YOUR BRIEF - AI-Powered Email Summary")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if args.email:
        print("Mode: Send via email 📧\n")
    else:
        print("Mode: Save to HTML 📄\n")

    try:
        # Step 1: Fetch emails from Gmail
        print("📥 Step 1: Fetching emails from Gmail...")
        emails = fetch_recent_emails(hours=24)

        if not emails:
            print("\n✅ No emails found in the last 24 hours.")
            print("Nothing to brief! Enjoy your quiet inbox 🎉")
            return

        print(f"   Found {len(emails)} emails\n")

        # Step 2: Classify emails with AI
        print("🤖 Step 2: Classifying emails with AI...")
        classifications = classify_emails(emails)
        print()

        # Step 3: Generate/send brief
        if args.email:
            # Send via email
            print("📧 Step 3: Sending brief via email...")
            success = send_brief_email(classifications)
            print()

            if success:
                print("=" * 60)
                print("✅ YOUR BRIEF HAS BEEN SENT!")
                print("=" * 60)
                print("\n📬 Check your inbox for your daily brief.\n")
            else:
                print("=" * 60)
                print("⚠️  FAILED TO SEND BRIEF")
                print("=" * 60)
                print("\n💡 Saving to HTML file as fallback...\n")
                output_file = generate_brief(classifications)
                print(f"📄 Brief saved to: {output_file}\n")
        else:
            # Save to HTML file
            print("📝 Step 3: Generating HTML brief...")
            output_file = generate_brief(classifications)
            print()

            print("=" * 60)
            print("✅ YOUR BRIEF IS READY!")
            print("=" * 60)
            print(f"\n📄 Brief saved to: {output_file}")
            print(f"\n💡 Open it in your browser:")
            print(f"   open {output_file}")
            print(f"\n   Or manually open the file in your browser\n")

        # Summary
        action_count = len([c for c in classifications if c['category'] == 'action'])
        if action_count > 0:
            print(f"⚠️  You have {action_count} action item(s) requiring attention")
        else:
            print("🎉 No action items today - all clear!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
