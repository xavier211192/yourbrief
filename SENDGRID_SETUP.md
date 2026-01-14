# SendGrid API Setup Guide

Follow these steps to get your SendGrid API key for sending email briefs.

## Overview

SendGrid is an email delivery service with a generous free tier:
- **100 emails/day forever free**
- More than enough for daily briefs
- Professional email delivery
- No credit card required for free tier

---

## Step 1: Sign Up for SendGrid

1. Go to: https://signup.sendgrid.com/
2. Fill in the signup form:
   - **Email:** Your email address
   - **Password:** Create a secure password
   - **Username:** Choose a username
3. Click **"Create Account"**
4. Check your email for verification link
5. Click the verification link to activate your account

---

## Step 2: Complete Account Setup

After verifying your email, you'll be asked a few questions:

1. **Tell us about yourself:**
   - Choose: "I'm exploring SendGrid" or "Personal project"
   - Click **"Next"**

2. **What's your role?**
   - Choose: "Developer" or "Individual"
   - Click **"Next"**

3. **What do you want to send?**
   - Choose: "Transactional emails" or "Personal emails"
   - Click **"Get Started"**

---

## Step 3: Create an API Key

1. Once in the dashboard, look for **"Settings"** in the left sidebar
2. Click **"Settings"** → **"API Keys"**
3. Or go directly to: https://app.sendgrid.com/settings/api_keys
4. Click the blue **"Create API Key"** button in the top right
5. Fill in the details:
   - **API Key Name:** `YourBrief` (or any name you want)
   - **API Key Permissions:** Select **"Full Access"** (simplest for MVP)
     - For production, you can use "Restricted Access" with just "Mail Send" permission
6. Click **"Create & View"**

---

## Step 4: Copy Your API Key

**IMPORTANT:** You can only see this key once!

1. You'll see a screen with your API key (starts with `SG.`)
2. Click **"Copy"** or manually copy the entire key
3. **Store it safely** - you won't be able to see it again
4. If you lose it, you'll need to create a new one

Example format: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy`

---

## Step 5: Verify Sender Identity

Before you can send emails, SendGrid needs to verify you own the sender email address.

### Option A: Single Sender Verification (Easiest for MVP)

1. In SendGrid dashboard, go to **"Settings"** → **"Sender Authentication"**
2. Or go to: https://app.sendgrid.com/settings/sender_auth
3. Under **"Single Sender Verification"**, click **"Get Started"** or **"Create New Sender"**
4. Fill in the form:
   - **From Name:** Your Brief (or your name)
   - **From Email Address:** Your email (e.g., yourname@gmail.com)
   - **Reply To:** Same as from email
   - **Company Address:** Your address (required, but can be home address)
   - **City, State, ZIP, Country:** Your location
5. Click **"Create"**
6. Check your email for a verification link from SendGrid
7. Click the verification link
8. Status should change to **"Verified"** ✅

### Option B: Domain Authentication (Better for Production)

If you have your own domain (e.g., yourdomain.com):
1. Go to **"Settings"** → **"Sender Authentication"**
2. Under **"Domain Authentication"**, click **"Get Started"**
3. Follow the wizard to add DNS records to your domain
4. This is more complex but gives better email delivery

**For MVP, use Option A (Single Sender Verification)**

---

## Step 6: Add API Key to Your Project

1. Open your `.env` file in the project
2. Find the SendGrid section:
   ```
   # SendGrid Email Configuration
   SENDGRID_API_KEY=SG.your-sendgrid-api-key-here
   SENDGRID_FROM_EMAIL=yourbrief@yourdomain.com
   SENDGRID_FROM_NAME=Your Brief
   ```

3. Update it with your actual values:
   ```
   SENDGRID_API_KEY=SG.actual_key_you_copied_from_step_4
   SENDGRID_FROM_EMAIL=your-verified-email@gmail.com
   SENDGRID_FROM_NAME=Your Brief
   ```

**Important:**
- `SENDGRID_FROM_EMAIL` must match the email you verified in Step 5
- `SENDGRID_FROM_NAME` is what shows as the sender name (can be anything)

---

## Step 7: Test Your Setup (Optional)

You can test SendGrid without writing code:

1. In SendGrid dashboard, go to **"Email API"** → **"Integration Guide"**
2. Or go to: https://app.sendgrid.com/guide/integrate
3. Choose **"Web API"** → **"Python"**
4. SendGrid will show you a test email command
5. You can send a test email to yourself to verify it works

---

## Verify Your Setup

Your `.env` file should now have:

```bash
# SendGrid Email Configuration
SENDGRID_API_KEY=SG.xxxxxxxxxxxx.yyyyyyyyyyyy
SENDGRID_FROM_EMAIL=your-verified-email@gmail.com
SENDGRID_FROM_NAME=Your Brief
```

And in SendGrid dashboard:
- ✅ API key created
- ✅ Sender email verified (green checkmark)

---

## Troubleshooting

**"Sender email not verified"**
- Check your email for SendGrid verification link
- Make sure you clicked the verification link
- Wait a few minutes and refresh the dashboard

**"403 Forbidden" error when sending**
- Your sender email is not verified
- The FROM email doesn't match the verified sender
- API key doesn't have "Mail Send" permission

**"Can't find API Keys in dashboard"**
- Look for **"Settings"** in left sidebar
- Click **"API Keys"** under Settings
- If still not visible, you might need to complete account setup first

**Lost your API key?**
- You can't retrieve it, but you can create a new one
- Go to Settings → API Keys → Create API Key
- Delete the old key if you want

**Want to test without building email service?**
- Use SendGrid's API test tool in dashboard
- Or use curl/Postman with your API key
- Check: https://docs.sendgrid.com/api-reference/mail-send/mail-send

---

## Next Steps

Once you have your SendGrid API key configured:

1. Build the email service (`app/services/email_service.py`)
2. Update `main.py` to send emails instead of saving HTML
3. Test sending yourself a brief
4. Set up daily scheduling with cron

---

## Free Tier Limits

- **100 emails/day forever free**
- No credit card required
- Enough for:
  - Daily brief (1 email/day)
  - Testing (99 emails/day left)
  - Small user base (100 users with 1 email/day)

To increase limits, upgrade to paid plan (starts at $19.95/month for 50,000 emails).

---

## Security Notes

- **Never commit** your API key to git (already in `.gitignore`)
- **Never share** your API key publicly
- **Rotate keys** periodically for security
- **Use restricted access** in production (only "Mail Send" permission)
- **Store API key** in `.env` file only

---

**Done!** You now have SendGrid configured and ready to send email briefs.

See `QUICKSTART.md` for instructions on using Your Brief with email delivery.
