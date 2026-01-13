# Your Brief - Product Specification

## 📋 Document Information

**Product Name:** Your Brief  
**Version:** 1.0 (MVP)  
**Last Updated:** January 2025  
**Status:** Ready to Build  
**Target Launch:** 4 weeks from start  

---

## 🎯 Product Overview

### What Is Your Brief?

Your Brief is an AI-powered email assistant that analyzes your Gmail inbox and sends **one daily morning brief** telling you exactly what needs your attention and what you can safely ignore.

**This is NOT:**
- An inbox UI replacement
- An email reply bot
- A generic email summarizer

**This IS:**
- A decision-focused briefing system
- A signal-from-noise filter
- A morning ritual for email clarity

---

## 💡 Core Value Proposition

> "Every morning, I get one short, trustworthy brief from Your Brief telling me exactly what needs my attention today — and what I can ignore."

### Expected User Outcomes

If the brief is accurate, users should:
- ✅ Spend <5 minutes on email triage vs 30+ minutes
- ✅ Feel confident they're not missing anything important
- ✅ Reduce email anxiety and decision fatigue
- ✅ Check Gmail <3 times per day vs 10+ times

---

## 👤 Target User (MVP)

### Primary Persona

**Role:** CEO / Founder / Business Owner / Manager

**Characteristics:**
- Uses Gmail as primary email
- Receives 50-200 emails per day
- Email = decision & coordination tool (not just communication)
- Suffers from inbox clutter, noise, and missed follow-ups
- Values time and wants to be proactive, not reactive

**Pain Points:**
- Overwhelmed by email volume
- Misses important messages in the noise
- Spends too much time triaging emails
- Constantly checking inbox for fear of missing something
- Struggles to prioritize what needs immediate attention

### Secondary Persona (Future)

- Knowledge workers
- Professionals overwhelmed by promotions and notifications
- Anyone who wants better email management

---

## 🎨 Product Design Philosophy

### Design Principles

1. **Radical Simplicity** - One brief, one time per day, maximum clarity
2. **Trust Through Accuracy** - Classification must be >85% accurate from day one
3. **Respectful of Time** - Brief must be scannable in under 60 seconds
4. **Non-Invasive** - Read-only access, no emails sent on user's behalf
5. **Continuous Learning** - Improve through feedback loop

### What Makes Your Brief Different

| Traditional Email Tools | Your Brief |
|------------------------|------------|
| Show you everything | Show you what matters |
| Real-time notifications | Once daily, morning ritual |
| Complex UI to learn | Delivered as simple email |
| Reactive (respond to pings) | Proactive (plan your day) |
| Feature bloat | Laser-focused on one thing |

---

## 🔧 MVP Technical Scope

### Input: What We Analyze

**Data Source:**
- Gmail inbox via Gmail API
- **Read-only access only** (no sending, no deleting)

**Email Scope:**
- Time window: Last 24-48 hours
- Focus areas:
  - Primary inbox (not Promotions/Social tabs)
  - Unread emails
  - Replied threads (to track waiting status)

**Email Fields Used:**
- Sender (name and email)
- Subject
- Snippet (preview text, ~200 chars)
- Timestamp
- To / CC recipients
- Thread ID
- Labels

**What We DON'T Store:**
- Full email bodies (privacy by design)
- Attachments
- Email content beyond 48 hours

### Output: What Users Receive

**Delivery Method:** HTML Email (with plain text fallback)

**Frequency:** Once per day

**Timing:** Morning (user-configurable, default 7:00 AM local time)

**Content Structure:**
1. **Header**: Date, overview stats
2. **🔴 Action Required** (max 5 items)
3. **🟡 Waiting On Others** (max 3 items)
4. **🟢 Info Only** (max 5 items)
5. **Summary**: Count of filtered emails

**Subject Line Format:**
```
Your Brief - Jan 14: 3 actions, 2 waiting
```

---

## 🏷️ Email Classification System

Every email/thread must be classified into **exactly ONE** category:

### 🔴 Action Required

**When to use:**
- Direct request to the user
- Question requiring response
- Approval or decision needed
- Task assigned to the user
- Deadline mentioned (explicit or implicit)

**Examples:**
- "Can you approve this budget by EOD?"
- "Need your input on the proposal"
- "Please review and sign the contract"

### 🟡 Waiting On Others

**When to use:**
- User already replied to the email
- Someone owes the user a response
- Follow-up required if no response received
- User is expecting deliverables from others

**Examples:**
- "Thanks, I'll send the revised contract by Friday" (after user gave feedback)
- "Let me check with the team and get back to you"
- User asked a question, waiting for answer

### 🟢 Info Only

**When to use:**
- FYIs and announcements
- Updates and status reports
- Internal communications
- Informational newsletters (legitimate)
- User is CC'd (usually info, not action)

**Examples:**
- "Weekly metrics report"
- "New employee announcement"
- "FYI - project completed phase 1"

### ⚪ Ignore / Noise

**When to use:**
- Promotional emails
- Marketing campaigns
- Automated notifications (no action needed)
- Social media updates
- Spam and junk

**Examples:**
- "50% off sale this weekend!"
- "You have 10 new LinkedIn notifications"
- Automated no-reply messages

---

## 📊 Information Extraction

For items classified as **Action Required** or **Waiting On**, extract:

### What's Needed
- **Format:** One clear sentence
- **Example:** "Review and approve Q1 marketing budget increase"
- **Goal:** User should understand immediately what to do

### Who's Involved
- **Format:** Sender name (and title if available)
- **Example:** "Sarah Chen (CFO)"
- **Goal:** Quick recognition of key stakeholders

### Deadline
- **Format:** Human-readable date/time
- **Examples:** "Today by 2pm", "EOD tomorrow", "Friday Jan 17"
- **Sources:** 
  - Explicit mentions: "by Friday", "before 5pm", "deadline is..."
  - Keywords: EOD, COB, ASAP, due date, by [date]
- **If none found:** null (don't make up deadlines)

### Priority Level
- **HIGH:** Explicit deadline within 24 hours, urgent language, critical decisions
- **MEDIUM:** Deadline within a week, important but not urgent
- **LOW:** No deadline, routine requests, can wait

---

## 🎚️ Prioritization Rules

### Prioritize HIGHER if:

1. **Direct addressing**: User is in "To:" field (not CC)
2. **Deadline mentioned**: Any time-bound language
3. **Multiple touches**: Same sender appears multiple times
4. **Thread activity**: Back-and-forth conversation (3+ messages)
5. **Long wait**: Email unanswered for 2+ days
6. **Urgency keywords**: "urgent", "ASAP", "critical", "emergency"
7. **Question to user**: Direct questions with "?"

### Prioritize LOWER if:

1. **CC'd only**: User not directly addressed
2. **No request**: Purely informational
3. **Automated sender**: no-reply@, automated@, notifications@
4. **Newsletter patterns**: "unsubscribe", "promotional", "update@"
5. **Social updates**: LinkedIn, Twitter, Facebook notifications

---

## 🤖 AI Classification Engine

### Technology Stack

**AI Provider:** OpenAI  
**Model:** GPT-4o (gpt-4o)  
**API:** OpenAI Chat Completions API

**Why GPT-4o:**
- Strong reasoning for email context understanding
- Excellent JSON output formatting
- Cost-effective for MVP ($2.50/M input, $10/M output tokens)
- Reliable and well-documented

### Classification Approach

**Method:** Few-shot prompting with structured output

**Prompt Components:**
1. System prompt with clear classification rules
2. 8 diverse example emails with expected classifications
3. Batch of emails to classify (up to 10 per API call)
4. Request for JSON array response

**Token Budget:**
- Average email: ~100-150 tokens
- System prompt: ~800 tokens
- Examples: ~1200 tokens
- Batch of 10 emails: ~1500 tokens
- **Total per batch:** ~3500 tokens input, ~1000 tokens output

**Cost per Brief:**
- Input: 3500 tokens × $2.50/M = $0.00875
- Output: 1000 tokens × $10/M = $0.01
- **Total:** ~$0.02 per brief (50 emails = 5 batches)

### Accuracy Requirements

**Target Metrics:**
- Overall classification accuracy: **>85%**
- Action category precision: **>90%** (critical - can't miss important emails)
- Ignore category recall: **>80%** (filter most noise)
- User satisfaction: **>70% thumbs up** on feedback

**Validation Strategy:**
- Confidence scoring on each classification
- Feedback collection after every brief
- Manual review of misclassifications
- Prompt tuning based on errors

---

## 📧 Brief Email Design

### Visual Design Principles

1. **Scannable** - User should grasp key items in 30 seconds
2. **Color-coded** - Categories instantly recognizable
3. **Mobile-friendly** - Looks great on phone (70% of email opens)
4. **Clean hierarchy** - Most important items first
5. **Actionable** - Direct links to Gmail for quick access

### Email Structure

```
┌─────────────────────────────────────────┐
│  ☀️ Your Brief                          │
│  Tuesday, January 14, 2025              │
│                                         │
│  Stats: 3 actions | 2 waiting |        │
│         8 info | 34 filtered           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🔴 ACTION REQUIRED (3)                 │
├─────────────────────────────────────────┤
│                                         │
│  [HIGH] Q1 Budget Approval Needed       │
│  From: Sarah Chen (CFO)                 │
│  What: Review and approve revised       │
│        Q1 marketing budget              │
│  Deadline: Tomorrow, Jan 15             │
│  [Open in Gmail]                        │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  [HIGH] Client escalation: DataCorp     │
│  From: Mike Rodriguez                   │
│  What: Decision on extension vs refund  │
│  Deadline: Today, 2pm PT                │
│  [Open in Gmail]                        │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  [MEDIUM] Board deck review             │
│  From: Jessica Wu (COO)                 │
│  What: Review financial projections     │
│  Deadline: Friday, Jan 17               │
│  [Open in Gmail]                        │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🟡 WAITING ON OTHERS (2)               │
├─────────────────────────────────────────┤
│                                         │
│  Partnership terms - TechVentures       │
│  From: Alex Kumar                       │
│  Waiting for: Revised contract          │
│  Since: 3 days ago                      │
│  [Send Follow-up]                       │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🟢 INFO ONLY (8)                       │
├─────────────────────────────────────────┤
│  • Weekly metrics report from Growth    │
│  • New employee announcement            │
│  • IT: Scheduled maintenance            │
│  [View all 8 items]                     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  34 emails were filtered                │
│  (newsletters, promotions, automated)   │
│                                         │
│  This brief analyzed 47 emails          │
│                                         │
│  [View in Browser] [Preferences]        │
│  [Give Feedback]                        │
└─────────────────────────────────────────┘
```

### Content Limits

To keep the brief scannable:
- **Action Required:** Max 5 items (prioritize by urgency)
- **Waiting On:** Max 3 items (show oldest first)
- **Info Only:** Max 5 items shown, count the rest
- **Total Brief Length:** Target 10-13 items

If more items exist, prioritize ruthlessly and note count of "Additional items" at bottom.

---

## 🗄️ Data Architecture

### Database: SQLite with SQLAlchemy

**Why SQLite for MVP:**
- Zero configuration
- File-based (easy backup)
- Perfect for single-user MVP
- Easy to migrate to PostgreSQL later

### Data Models

#### 1. Email
Stores fetched email metadata (48-hour retention).

```python
- id: Primary key
- gmail_id: Unique Gmail message ID
- thread_id: Gmail thread ID
- sender_name: Parsed sender name
- sender_email: Parsed sender email
- subject: Email subject
- snippet: Preview text (~200 chars)
- received_date: When email was received
- labels: JSON array of Gmail labels
- is_automated: Boolean (detected bot)
- has_questions: Boolean (contains ?)
- question_count: Integer
- is_urgent: Boolean (urgent keywords)
- deadline_keywords: JSON array
- raw_data: JSON blob (full metadata)
- created_at, updated_at: Timestamps
```

#### 2. Classification
AI classification results linked to emails.

```python
- id: Primary key
- email_id: Foreign key to Email
- category: action/waiting/info/ignore
- priority: high/medium/low
- what_needed: Description text
- deadline: Datetime (extracted)
- deadline_text: Original deadline text
- confidence_score: 0.0-1.0 float
- ai_reasoning: Why classified this way
- model_used: "gpt-4o"
- classified_at: Timestamp
```

#### 3. UserPreferences
User configuration and settings.

```python
- id: Primary key
- user_email: User's email (unique)
- delivery_time: "HH:MM" format
- timezone: IANA timezone string
- enabled: Boolean (active/paused)
- max_action_items: Integer (default 5)
- max_waiting_items: Integer (default 3)
- max_info_items: Integer (default 5)
- include_weekends: Boolean (default false)
- last_brief_sent: Datetime
- total_briefs_sent: Integer counter
- created_at, updated_at: Timestamps
```

#### 4. Feedback
User feedback on classifications.

```python
- id: Primary key
- classification_id: Foreign key
- feedback_type: thumbs_up/thumbs_down
- user_comment: Optional text
- submitted_at: Timestamp
```

#### 5. Brief
Record of sent briefs for analytics.

```python
- id: Primary key
- user_email: Recipient email
- sent_at: When brief was sent
- total_emails_analyzed: Count
- action_count: Count
- waiting_count: Count
- info_count: Count
- ignored_count: Count
- email_sent_successfully: Boolean
- sendgrid_message_id: Tracking ID
- brief_data: JSON blob (full brief)
- created_at: Timestamp
```

### Data Retention Policy

**Privacy by Design:**
- Email raw data: **48 hours** then purged
- Classifications: **30 days** (for analytics)
- Briefs: **90 days** (for history)
- User preferences: Until account deletion
- Feedback: Indefinitely (for improvement)

---

## 🔄 System Architecture

### Core Services

```
┌─────────────────────────────────────────┐
│         Daily Scheduler                 │
│         (APScheduler)                   │
│  Triggers at 7:00 AM user's timezone   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Orchestrator Service            │
│  Coordinates full pipeline              │
└──────────────┬──────────────────────────┘
               │
               ▼
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────┐         ┌─────────┐
│  Gmail  │         │   AI    │
│ Service │────────▶│Classifier│
│         │         │ Service │
└────┬────┘         └────┬────┘
     │                   │
     ▼                   ▼
┌─────────┐         ┌─────────┐
│  Email  │         │  Brief  │
│ Cleaner │────────▶│Generator│
└─────────┘         └────┬────┘
                         │
                         ▼
                    ┌─────────┐
                    │SendGrid │
                    │ Service │
                    └─────────┘
```

### Service Descriptions

**1. Gmail Service**
- Authenticates with OAuth 2.0
- Fetches emails from last 24 hours
- Parses email metadata
- Handles API rate limits

**2. Email Cleaner**
- Removes promotional emails
- Filters automated notifications
- Deduplicates by thread
- Enriches with metadata

**3. AI Classifier**
- Batches emails (10 per batch)
- Calls OpenAI GPT-4o API
- Parses JSON responses
- Validates classifications

**4. Brief Generator**
- Aggregates classifications
- Prioritizes items
- Limits item counts
- Formats brief data

**5. SendGrid Service**
- Renders HTML email template
- Sends via SendGrid API
- Tracks delivery status
- Logs errors

**6. Orchestrator**
- Runs full pipeline
- Handles errors gracefully
- Logs each step
- Updates database

**7. Scheduler**
- Triggers daily at configured time
- Respects user timezone
- Skips weekends if configured
- Handles failures without crashing

---

## 🚀 MVP Development Timeline

### Phase 1: Foundation (Week 1)
**Days 1-2:**
- ✅ Project setup with UV
- ✅ Gmail API authentication
- ✅ Email fetching service

**Days 3-5:**
- ✅ Email parsing & cleaning
- ✅ Database models & schema
- ✅ Sample data collection

**Days 6-7:**
- ✅ Test all components
- ✅ Verify data pipeline

### Phase 2: AI Classification (Week 2)
**Days 8-10:**
- ✅ Prompt engineering
- ✅ OpenAI API integration
- ✅ Classification validation

**Days 11-14:**
- ✅ Batch processing
- ✅ Cost optimization
- ✅ Accuracy testing

### Phase 3: Brief Generation (Week 3)
**Days 15-17:**
- ✅ Brief data aggregation
- ✅ HTML email templates
- ✅ SendGrid integration

**Days 18-21:**
- ✅ Template testing
- ✅ Email delivery testing
- ✅ Error handling

### Phase 4: Automation (Week 4)
**Days 22-24:**
- ✅ Daily scheduler
- ✅ User preferences
- ✅ Feedback collection

**Days 25-28:**
- ✅ End-to-end testing
- ✅ Documentation
- ✅ Deployment prep
- ✅ Launch to self

---

## 📊 Success Metrics

### MVP Success Criteria

**Technical Metrics:**
- ✅ Classification accuracy >85%
- ✅ Brief generation time <60 seconds
- ✅ Email delivery success rate >99%
- ✅ Zero data breaches or security incidents

**User Metrics:**
- ✅ User checks Gmail <3 times/day (vs 10+ before)
- ✅ User reports <5 min/day on email triage (vs 30+ before)
- ✅ User feedback: >70% thumbs up on classifications
- ✅ User retention: 30+ consecutive days of usage

**Business Metrics:**
- ✅ Cost per brief: <$0.05
- ✅ Time to generate brief: <2 minutes
- ✅ User satisfaction score: 4+/5 stars

### Post-MVP Metrics

**Engagement:**
- Daily active users (DAU)
- Brief open rate
- Feedback submission rate
- Average items per brief

**Product Quality:**
- Classification accuracy by category
- False positive rate (important emails marked ignore)
- False negative rate (noise marked action)
- Time saved per user

**Growth:**
- User acquisition rate
- Retention curve (D1, D7, D30)
- Referral rate
- Paid conversion rate

---

## 🔐 Security & Privacy

### Data Security

**Principles:**
1. **Read-Only Access:** Gmail API is read-only, no sending/deleting
2. **Local Storage:** All data stored locally on user's machine
3. **Encryption at Rest:** SQLite database encrypted
4. **No Cloud Storage:** Email content never sent to external servers
5. **Token Security:** OAuth tokens stored securely, gitignored

### Privacy Guarantees

**What We Store:**
- Email metadata (sender, subject, snippet)
- Only for 48 hours
- No full email bodies
- No attachments

**What We DON'T Store:**
- Email body content
- Attachments
- Deleted emails
- Archived emails

**User Control:**
- Users can revoke access anytime
- Users can delete all data
- Users can export their data
- Users can pause briefs anytime

### Compliance

**MVP Scope:**
- GDPR: Right to access, delete, export data
- Privacy Policy: Clear explanation of data usage
- Terms of Service: Standard SaaS terms

**Future:**
- SOC 2 Type II certification
- HIPAA compliance (if needed)
- Enterprise security features

---

## 🎨 User Experience Flow

### First-Time Setup (5 minutes)

1. **Install & Run:**
   - Clone repo
   - Run setup script
   - Install dependencies

2. **Gmail Authentication:**
   - Create Google Cloud project
   - Enable Gmail API
   - Download credentials
   - Complete OAuth flow

3. **Configure Preferences:**
   - Set delivery time (default 7:00 AM)
   - Set timezone
   - Choose weekdays only or include weekends

4. **Test Brief:**
   - Run manual brief generation
   - Verify email received
   - Check classification accuracy

### Daily Usage (60 seconds)

1. **Receive Brief:**
   - Email arrives at 7:00 AM
   - Subject shows summary: "Your Brief - 3 actions, 2 waiting"

2. **Scan Brief:**
   - Read action items (30 seconds)
   - Note waiting items (10 seconds)
   - Acknowledge info items (10 seconds)

3. **Take Action:**
   - Click "Open in Gmail" for important items
   - Mark items as done (future feature)
   - Provide feedback (thumbs up/down)

### Feedback Loop (10 seconds)

1. **Spot Misclassification:**
   - Notice important email marked as "info"

2. **Provide Feedback:**
   - Click thumbs down button
   - Email marked for review

3. **System Learns:**
   - Prompt adjusted based on feedback
   - Future briefs improve

---

## 🛠️ Technology Stack

### Core Technologies

**Language:** Python 3.11+  
**Package Manager:** UV (modern, fast)  
**Web Framework:** Flask 3.0  
**Database:** SQLite + SQLAlchemy  
**AI:** OpenAI GPT-4o  
**Email API:** Gmail API (read-only)  
**Email Sending:** SendGrid  
**Scheduling:** APScheduler  
**Templates:** Jinja2  

### Key Libraries

```python
flask==3.0.0                    # Web framework
google-auth==2.25.2             # Gmail auth
google-auth-oauthlib==1.2.0     # OAuth flow
google-api-python-client==2.108.0  # Gmail API
openai==1.54.0                  # OpenAI API
sqlalchemy==2.0.23              # ORM
python-dotenv==1.0.0            # Config
apscheduler==3.10.4             # Scheduling
sendgrid==6.11.0                # Email sending
jinja2==3.1.2                   # Templates
```

### Development Tools

- **UV:** Package management
- **Git:** Version control
- **Pytest:** Unit testing (future)
- **Black:** Code formatting (future)
- **SQLite Browser:** Database inspection

### Deployment (Future)

**MVP:** Local machine (cron job)  
**Production Options:**
- Railway (easy deployment)
- Render (free tier available)
- DigitalOcean App Platform
- AWS Lambda (serverless)

---

## 🚧 Out of Scope (MVP)

### Features NOT in MVP

❌ **Web Dashboard:** No browser UI, email-only  
❌ **Reply Suggestions:** No AI-powered replies  
❌ **Multi-User:** Single user only (you)  
❌ **Mobile App:** Email is mobile-friendly enough  
❌ **Slack Integration:** Email delivery only  
❌ **Custom Rules:** No user-defined filters yet  
❌ **Email Snoozing:** No postponing emails  
❌ **Calendar Integration:** No meeting context  
❌ **Contact Management:** No CRM features  
❌ **Analytics Dashboard:** Basic logging only  
❌ **Team Briefs:** Personal use only  

### Why These Are Excluded

**MVP Philosophy:** 
- Validate core value prop first
- One feature done exceptionally well
- Ship fast, learn fast, iterate

**Post-MVP Roadmap:**
These features become relevant after proving:
1. Users want daily email briefs
2. Classification accuracy is trustworthy
3. Users save significant time
4. Product-market fit is validated

---

## 🔮 Future Enhancements

### Phase 2: Web Dashboard (Week 5-6)
- Interactive web interface
- Mark items as complete
- Historical brief archive
- User preferences UI

### Phase 3: Advanced Features (Week 7-10)
- Custom classification rules
- Smart follow-up reminders
- Email threading context
- Sender relationship tracking

### Phase 4: Integrations (Week 11-14)
- Slack notifications
- Calendar context awareness
- Task management sync (Todoist, Asana)
- CRM integration (for sales users)

### Phase 5: Team Features (Month 4+)
- Shared team briefs
- Delegation workflows
- Team analytics
- Multi-user accounts

---

## 💰 Cost Analysis

### MVP Operating Costs (Per User Per Month)

**OpenAI API:**
- 30 briefs/month × $0.02/brief = **$0.60/month**

**SendGrid:**
- 30 emails/month = **Free tier** (100 emails/day limit)

**Infrastructure:**
- Local machine = **$0/month**

**Total MVP Cost:** **$0.60/month per user**

### Scaling Costs (100 Users)

**OpenAI API:**
- 100 users × 30 briefs × $0.02 = **$60/month**

**SendGrid:**
- Still free tier (3,000 emails/month < 100/day limit)

**Infrastructure:**
- Railway/Render: **$5-20/month**

**Total:** **~$80/month for 100 users**

### Revenue Potential (Future)

**Pricing Model Ideas:**
- Free: 14-day trial
- Personal: $9/month (individual users)
- Professional: $19/month (advanced features)
- Team: $49/month (5 users, team features)

**Break-Even:**
- 1 paying user covers 15 free users
- 10 users = $90/month revenue vs $10 cost

---

## 📝 Key Decisions & Rationale

### Why Email Delivery (Not Web Dashboard)?

**Pros:**
- Zero adoption friction
- Users already check email
- Mobile-friendly by default
- No login required
- Searchable/archivable

**Cons:**
- Limited interactivity
- Adds one more email to inbox

**Decision:** Start with email, add dashboard later if needed.

---

### Why OpenAI GPT-4o (Not Claude)?

**Pros:**
- Excellent JSON output formatting
- Strong reasoning capabilities
- Cost-effective ($2.50/M input tokens)
- Reliable and well-documented
- Function calling support

**Cons:**
- Slightly more expensive than some alternatives

**Decision:** GPT-4o offers best balance of quality and cost for MVP.

---

### Why SQLite (Not PostgreSQL)?

**Pros:**
- Zero configuration
- File-based, easy backup
- Perfect for single-user MVP
- No server management

**Cons:**
- Doesn't scale to multi-user

**Decision:** SQLite for MVP, easy migration path to PostgreSQL later.

---

### Why Once Daily (Not Real-Time)?

**Pros:**
- Prevents notification fatigue
- Encourages batching
- Simpler infrastructure
- Forces prioritization

**Cons:**
- Not suitable for time-critical emails

**Decision:** Daily cadence aligns with "morning ritual" concept. Real-time alerts defeat the purpose.

---

## 🎯 Open Questions to Validate

### Classification Accuracy
- Will 85% accuracy be enough for trust?
- How often will important emails be missed?
- What's acceptable false positive rate?

### User Behavior
- Will users actually check the brief daily?
- Will they trust AI classifications?
- How often will they need to open Gmail anyway?

### Timing
- Is morning optimal for everyone?
- Should we offer multiple brief times?
- What about different timezones?

### Content
- Is 10-13 items the right limit?
- Should we show more context?
- Do users want to see ignored emails?

---

## 📚 References & Resources

### Documentation Links
- Gmail API: https://developers.google.com/gmail/api
- OpenAI API: https://platform.openai.com/docs
- SendGrid API: https://docs.sendgrid.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Flask: https://flask.palletsprojects.com/
- APScheduler: https://apscheduler.readthedocs.io/

### Inspiration
- Hey (email service) - radical simplicity
- Superhuman - keyboard shortcuts & speed
- Notion AI - AI-powered workflows
- Morning Brew - daily brief format

---

## 🎬 Getting Started

See the accompanying **BUILD_GUIDE.md** for step-by-step instructions to build Your Brief using Claude Code.

---

**Document Version:** 1.0  
**Last Updated:** January 14, 2025  
**Next Review:** After MVP launch  
**Maintained By:** Your Brief Team