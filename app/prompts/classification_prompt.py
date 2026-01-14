"""
AI Prompt for email classification.

Based on prod-spec.md classification rules.
"""

SYSTEM_PROMPT = """You are an email classification assistant for "Your Brief" - a service that helps users identify what emails need attention.

Your job is to classify emails into exactly ONE of these categories:

🔴 ACTION REQUIRED - Use when:
- Direct request to the user
- Question requiring response
- Approval or decision needed
- Task assigned to the user
- Deadline mentioned (explicit or implicit)
Examples: "Can you approve this?", "Need your input", "Please review and sign"

🟡 WAITING ON OTHERS - Use when:
- User already replied to the email
- Someone owes the user a response
- Follow-up required if no response received
- User is expecting deliverables from others
Examples: "Thanks, I'll send it by Friday", "Let me check and get back to you"

🟢 INFO ONLY - Use when:
- FYIs and announcements
- Updates and status reports
- Internal communications
- Informational newsletters (legitimate)
- User is CC'd (usually info, not action)
Examples: "Weekly metrics report", "New employee announcement", "FYI - project completed"

⚪ IGNORE / NOISE - Use when:
- Promotional emails
- Marketing campaigns
- Automated notifications (no action needed)
- Social media updates
- Spam and junk
Examples: "50% off sale!", "LinkedIn notifications", automated no-reply messages

For ACTION REQUIRED and WAITING ON emails, also extract:
- what_needed: One clear sentence describing what's needed
- deadline: Human-readable deadline if mentioned (e.g., "Today by 2pm", "Friday Jan 17", or null if none)
- priority: HIGH (deadline within 24h), MEDIUM (within a week), or LOW (no deadline)

Return your response as a JSON array with one object per email."""


EXAMPLES = """
EXAMPLE CLASSIFICATIONS:

Email 1:
From: Sarah Chen <sarah@company.com>
Subject: Q1 Budget Approval Needed
Snippet: Hi, can you review and approve the revised Q1 marketing budget by EOD tomorrow? We need to finalize before the board meeting.

Classification:
{
  "category": "action",
  "priority": "high",
  "what_needed": "Review and approve revised Q1 marketing budget",
  "deadline": "Tomorrow EOD"
}

---

Email 2:
From: LinkedIn <notifications@linkedin.com>
Subject: You have 10 new notifications
Snippet: See who's viewed your profile this week. Connect with people you may know.

Classification:
{
  "category": "ignore",
  "priority": null,
  "what_needed": null,
  "deadline": null
}

---

Email 3:
From: Alex Kumar <alex@techventures.com>
Subject: Re: Partnership Agreement
Snippet: Thanks for the feedback! I'll send you the revised contract by Friday.

Classification:
{
  "category": "waiting",
  "priority": "medium",
  "what_needed": "Revised partnership contract from Alex",
  "deadline": "Friday"
}

---

Email 4:
From: Growth Team <team@company.com>
Subject: Weekly Metrics Report - Jan 14
Snippet: Here's your weekly summary: 1,234 signups, 89% retention, $45K revenue.

Classification:
{
  "category": "info",
  "priority": null,
  "what_needed": null,
  "deadline": null
}

---

Email 5:
From: Shop Now <deals@retailer.com>
Subject: 🔥 Flash Sale! 50% Off Everything Today Only
Snippet: Don't miss out! Limited time offer. Shop now before midnight.

Classification:
{
  "category": "ignore",
  "priority": null,
  "what_needed": null,
  "deadline": null
}

---

Email 6:
From: Mike Rodriguez <mike@datacorp.com>
Subject: URGENT: Client escalation - need decision by 2pm PT
Snippet: DataCorp is asking for either a 30-day extension or full refund. Need your call on this ASAP - client meeting at 2pm PT today.

Classification:
{
  "category": "action",
  "priority": "high",
  "what_needed": "Decide on DataCorp extension vs refund",
  "deadline": "Today 2pm PT"
}

---

Email 7:
From: HR Team <hr@company.com>
Subject: Office closed Monday for holiday
Snippet: Reminder: Office will be closed Monday, Jan 20 for MLK Day. Enjoy the long weekend!

Classification:
{
  "category": "info",
  "priority": null,
  "what_needed": null,
  "deadline": null
}

---

Email 8:
From: Jessica Wu <jessica@company.com>
Subject: Board deck - please review financial projections
Snippet: Can you review slides 12-15 (financial projections) before our board meeting on Friday? Want to make sure numbers align with your forecast.

Classification:
{
  "category": "action",
  "priority": "medium",
  "what_needed": "Review financial projections in board deck (slides 12-15)",
  "deadline": "Friday"
}
"""


def build_classification_prompt(emails: list) -> str:
    """
    Build the full prompt with examples and emails to classify.

    Args:
        emails: List of email dicts from Gmail service

    Returns:
        Full prompt string for OpenAI
    """
    # Start with examples
    prompt = EXAMPLES + "\n\nNOW CLASSIFY THESE EMAILS:\n\n"

    # Add each email to classify
    for i, email in enumerate(emails, 1):
        prompt += f"""Email {i}:
From: {email['sender_name']} <{email['sender_email']}>
Subject: {email['subject']}
Snippet: {email['snippet']}

---

"""

    # Add instructions for response format
    prompt += """
Return a JSON object with this structure:
{
  "classifications": [
    {
      "category": "...",
      "priority": "..." or null,
      "what_needed": "..." or null,
      "deadline": "..." or null
    },
    ... (one object per email in the same order)
  ]
}

Category must be one of: "action", "waiting", "info", "ignore"
Priority must be one of: "high", "medium", "low", or null
"""

    return prompt
