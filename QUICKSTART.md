# Quick Start - Your Brief MVP

## Prerequisites (One-Time Setup)

You should have already completed:
- ✅ Gmail API setup with `credentials.json` in project root
- ✅ OpenAI API key added to `.env` file
- ✅ Dependencies installed with `uv sync`

If not, see [GMAIL_SETUP.md](GMAIL_SETUP.md) for Gmail setup.

---

## Generate Your Daily Brief

### Option 1: Save to HTML (Default)

```bash
uv run python main.py
```

**What happens:**
1. 📥 Fetches your emails from Gmail (last 24 hours)
2. 🤖 Classifies them with AI
3. 📝 Generates a beautiful HTML brief
4. 💾 Saves to `brief_output.html`
5. 🌐 Opens automatically in your browser

### Option 2: Send via Email

```bash
uv run python main.py --email
```

**What happens:**
1. 📥 Fetches your emails from Gmail (last 24 hours)
2. 🤖 Classifies them with AI into categories:
   - 🔴 Action Required
   - 🟡 Waiting On Others
   - 🟢 Info Only
   - ⚪ Ignore/Noise (filtered out)
3. 📧 Sends formatted brief to your email via SendGrid

**Requires:** SendGrid API key configured in `.env` (see [SENDGRID_SETUP.md](SENDGRID_SETUP.md))

### What You'll See in Your Brief

- **Action items** with priorities and deadlines
- **Waiting items** you're tracking
- **Info-only items** summarized
- **Filtered count** of promotional emails removed
- **Direct links** to open each email in Gmail

### Cost

~$0.02 per brief (OpenAI API usage)

---

## Example Output

```
============================================================
☀️  YOUR BRIEF - AI-Powered Email Summary
============================================================

📥 Step 1: Fetching emails from Gmail...
   Found 15 emails

🤖 Step 2: Classifying emails with AI...
   ✅ Classified 15 emails successfully

📝 Step 3: Generating HTML brief...
   📊 Brief Summary:
      🔴 Action Required: 2
      🟡 Waiting On Others: 0
      🟢 Info Only: 4
      ⚪ Filtered: 9

============================================================
✅ YOUR BRIEF IS READY!
============================================================

📄 Brief saved to: /path/to/brief_output.html

⚠️  You have 2 action item(s) requiring attention
```

---

## Testing Individual Components (Optional)

### Test Gmail Connection

Fetch and display your recent emails:

```bash
uv run python app/services/gmail_service.py
```

Shows: sender, subject, snippet, and date for recent emails.

### Test AI Classifier

Classify emails and see category breakdown:

```bash
uv run python app/services/classifier_service.py
```

Shows: classification summary and action items with details.

### Test Brief Generator

Generate brief from existing classifications:

```bash
uv run python app/services/brief_generator.py
```

Shows: HTML brief generation with category counts.

---

## Daily Usage Workflow

1. **Morning:** Run `uv run python main.py`
2. **Review:** Open `brief_output.html` in browser
3. **Act:** Click links to open important emails in Gmail
4. **Done:** Close and enjoy your organized day!

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'app'"**
- Make sure you're running from the project root directory
- Use `uv run python main.py` (not `python app/...`)

**"Gmail authentication failed"**
- Make sure `credentials.json` exists in project root
- Delete `token.pickle` and re-authenticate if needed

**"OpenAI API error"**
- Check your API key in `.env` file
- Verify you have credits at https://platform.openai.com/

**Brief doesn't open automatically**
- Manually open `brief_output.html` in your browser
- Or run: `open brief_output.html` (macOS) / `start brief_output.html` (Windows)

---

## Next Steps (Future Enhancements)

Once you're happy with the basic MVP:

1. **Email delivery** - Send brief to your email instead of saving to file
2. **Scheduling** - Automate daily briefs with cron job or task scheduler
3. **Feedback loop** - Add thumbs up/down to improve classifications
4. **Database** - Track processed emails to avoid duplicates
5. **Web dashboard** - View briefs history and manage preferences

---

## Files Generated

- `brief_output.html` - Your daily brief (safe to delete, regenerates each run)
- `token.pickle` - Gmail authentication token (gitignored, keep this)

---

**Questions?** Check [README.md](README.md) for project overview or [prod-spec.md](prod-spec.md) for full specification.
