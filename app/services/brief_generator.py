"""
Brief Generator - Create HTML brief from classified emails.
"""
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def generate_brief(classifications: List[Dict[str, Any]], output_file: str = "brief_output.html") -> str:
    """
    Generate HTML brief from classified emails and save to file.

    Args:
        classifications: List of classified email dicts
        output_file: Path to output HTML file (default: brief_output.html)

    Returns:
        Path to generated HTML file
    """
    print(f"📝 Generating brief from {len(classifications)} classified emails...")

    # Organize emails by category
    action_items = [c for c in classifications if c['category'] == 'action']
    waiting_items = [c for c in classifications if c['category'] == 'waiting']
    info_items = [c for c in classifications if c['category'] == 'info']
    ignore_items = [c for c in classifications if c['category'] == 'ignore']

    # Sort action items by priority (high -> medium -> low)
    priority_order = {'high': 0, 'medium': 1, 'low': 2, None: 3}
    action_items.sort(key=lambda x: priority_order.get(x.get('priority'), 3))

    # Limit items per section (as per prod spec)
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
    }

    # Set up Jinja2 environment
    template_dir = Path(__file__).parent.parent.parent / 'templates'
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template('brief_email.html')

    # Render template
    html_content = template.render(**template_data)

    # Save to file
    output_path = Path(output_file)
    output_path.write_text(html_content, encoding='utf-8')

    print(f"✅ Brief generated successfully!")
    print(f"📄 Saved to: {output_path.absolute()}")
    print(f"\n📊 Brief Summary:")
    print(f"   🔴 Action Required: {template_data['action_count']}")
    print(f"   🟡 Waiting On Others: {template_data['waiting_count']}")
    print(f"   🟢 Info Only: {template_data['info_count']}")
    print(f"   ⚪ Filtered: {template_data['ignore_count']}")

    return str(output_path.absolute())


if __name__ == '__main__':
    """Quick test of brief generator."""
    from app.services.gmail_service import fetch_recent_emails
    from app.services.classifier_service import classify_emails

    # Fetch and classify emails
    print("🔍 Fetching emails...")
    emails = fetch_recent_emails(hours=24)

    if not emails:
        print("No emails to generate brief from")
        exit(0)

    print("🤖 Classifying emails...")
    classifications = classify_emails(emails)

    # Generate brief
    output_file = generate_brief(classifications)

    print(f"\n✨ Done! Open this file in your browser:")
    print(f"   {output_file}")
    print(f"\nOr run: open {output_file}")
