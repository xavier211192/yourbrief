# Gmail API Setup Guide

Follow these steps to get your `credentials.json` file.

## Step 1: Go to Google Cloud Console

1. Visit: https://console.cloud.google.com/
2. Sign in with your Google account (the one with the Gmail you want to analyze)

## Step 2: Create a New Project

1. Click the project dropdown at the top
2. Click **"New Project"**
3. Name it: `YourBrief` (or anything you want)
4. Click **"Create"**
5. Wait for project creation (~30 seconds)

## Step 3: Enable Gmail API

1. Make sure your new project is selected (check top dropdown)
2. Go to: https://console.cloud.google.com/apis/library
3. Search for: **"Gmail API"**
4. Click on **"Gmail API"** from results
5. Click the blue **"Enable"** button
6. Wait for it to enable (~10 seconds)

## Step 4: Configure OAuth Consent Screen

**Navigation (if link doesn't work):**
- In Google Cloud Console: Left menu → **APIs & Services** → **OAuth consent screen**

1. If not already there, go to: https://console.cloud.google.com/apis/credentials/consent
   - OR manually navigate: Left sidebar → APIs & Services → OAuth consent screen

2. **If you see "Google auth platform not configured yet":**
   - Look for a button that says **"Configure Consent Screen"** or **"Get Started"**
   - Click it
   - This takes you to the user type selection screen

3. Select **"External"** user type

4. Click **"Create"**

5. Fill in **required fields only** (App information page):
   - **App name:** YourBrief
   - **User support email:** Select your email from dropdown
   - Scroll down to **Developer contact information**
   - **Email addresses:** Your email
   - Leave everything else blank/default

6. Click **"Save and Continue"**

7. **Scopes page:** Just click **"Save and Continue"** (don't add anything)

8. **Test users page:**
   - Click **"+ Add Users"**
   - Enter your Gmail address
   - Click **"Add"**
   - Click **"Save and Continue"**

9. **Summary page:** Review and click **"Back to Dashboard"**

## Step 5: Create OAuth Credentials

1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **"+ Create Credentials"** at the top
3. Select **"OAuth client ID"**
4. Choose application type: **"Desktop app"**
5. Name it: **"YourBrief Desktop"**
6. Click **"Create"**
7. You'll see a popup with your credentials

## Step 6: Download credentials.json

1. In the popup (or credentials list), click the **Download** icon (⬇️)
2. This downloads a JSON file (usually named like `client_secret_xxx.json`)
3. **Rename it to:** `credentials.json`
4. **Move it to:** Your project root directory (`/Users/jennifer/Documents/source/yourbrief/`)

## Step 7: Verify File Location

Your project should now look like:
```
yourbrief/
├── credentials.json   ← This file!
├── app/
├── templates/
├── .env.example
└── ...
```

## Step 8: Test Connection

Run the Gmail service test:
```bash
cd /Users/jennifer/Documents/source/yourbrief
uv run python app/services/gmail_service.py
```

**What happens:**
1. Browser opens automatically
2. Google asks you to sign in
3. Google shows permissions: "YourBrief wants to read your Gmail"
4. Click **"Allow"**
5. See "Authentication successful" message
6. Browser tab closes
7. Script fetches and displays your recent emails

## Troubleshooting

**"Access blocked: This app hasn't been verified"**
- Click "Advanced" → "Go to YourBrief (unsafe)"
- This is normal for personal projects not published to Google

**"Invalid credentials"**
- Make sure `credentials.json` is in the project root
- Check file isn't corrupted (should be valid JSON)
- Try downloading credentials again from Google Cloud Console

**"API not enabled"**
- Go back to Step 3 and ensure Gmail API is enabled
- Wait a minute and try again

## Security Notes

- `credentials.json` contains your OAuth client secret
- Already added to `.gitignore` - never commit this file
- `token.pickle` will be created after first auth - also in `.gitignore`
- These files give read-only access to your Gmail

---

**Ready?** Let me know when you have `credentials.json` and want to test!
