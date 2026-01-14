# Your Brief - Simple MVP

AI-powered email brief generator that analyzes your Gmail inbox and creates a daily summary.

## Philosophy

**Keep it simple. Focus on value delivery first.**

This MVP has no database, no web server, no scheduling. Just one script that:
1. Fetches emails from Gmail (last 24 hours)
2. Classifies them with AI (action/waiting/info/ignore)
3. Generates an HTML brief
4. Sends it to your email

## Project Structure

```
yourbrief/
├── app/
│   ├── services/
│   │   ├── gmail_service.py      # Fetch emails from Gmail
│   │   ├── classifier_service.py  # Classify with OpenAI
│   │   └── email_service.py       # Send via SendGrid
│   └── prompts/
│       └── classification_prompt.py # AI prompt for classification
├── templates/
│   └── brief_email.html           # Email template
├── main.py                        # Run this to generate a brief
├── .env.example                   # Copy to .env and configure
└── prod-spec.md                   # Full product specification
```

## Setup

1. **Copy environment config:**
   ```bash
   cp .env.example .env
   ```

2. **Configure .env:**
   - Add your OpenAI API key
   - Add your SendGrid API key
   - Add your Gmail credentials path
   - Set your email address

3. **Set up Gmail API:**
   - Go to Google Cloud Console
   - Enable Gmail API
   - Download credentials.json to project root

4. **Install dependencies:**
   ```bash
   uv sync
   ```

## Usage

```bash
# Generate and send a brief
uv run python main.py
```

That's it!

## Next Steps (After MVP Works)

- Add database to track processed emails
- Add scheduling for daily briefs
- Add feedback mechanism
- Add user preferences
- Build web dashboard

## See Also

- `prod-spec.md` - Full product specification with all features planned

- Scope - Possibility to add hyperlink to the email and also classify as something that can should be unsubscribed direct link to unsubscribe