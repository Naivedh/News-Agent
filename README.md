# AI News Agent

Automated daily market news briefing system that fetches tech and financial news, analyzes it with AI, and emails a summary every morning.

## Features

- 📰 Fetches from 8 RSS feeds (WSJ, Reuters, TechCrunch, CNBC, Bloomberg, Cointelegraph)
- 🤖 AI analysis using Groq API (Llama 3.3 70B) to identify top 7-10 market-moving stories
- 📧 HTML email delivery via Resend API with professional formatting
- ⏰ Automated daily execution via GitHub Actions
- 🔒 Secure API key management with GitHub Secrets

## Quick Start

### 1. Fork/Clone this repo

### 2. Add GitHub Secrets
Go to: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Add these 4 secrets:
- `GROQ_API_KEY` - Get from https://console.groq.com (free)
- `RESEND_API_KEY` - Get from https://resend.com/api-keys (free, 100 emails/day)
- `FROM_EMAIL_NEWS_AGENT` - Use `onboarding@resend.dev`
- `RECIPIENT_EMAIL_NEWS_AGENT` - Your email address

### 3. Test the Workflow
- Go to `Actions` tab
- Click `Daily News Briefing`
- Click `Run workflow` → `Run workflow`
- Check your email!

### 4. Automatic Daily Runs
The workflow runs automatically every day at 8 AM PST (4 PM UTC). No further action needed!

## Local Development

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Create `.env` file:
```bash
GROQ_API_KEY=your_key_here
RESEND_API_KEY=your_key_here
FROM_EMAIL=onboarding@resend.dev
RECIPIENT_EMAIL=your_email@example.com
```

3. Run manually:
```bash
python3 news_agent.py
```

## Cost

**$0/month** - All services on free tier, no credit card required.

## Stopping the Workflow

To stop daily emails:
```bash
git rm .github/workflows/news.yml
git commit -m "chore: remove daily news workflow"
git push
```

## News Sources

- WSJ Markets & Business
- Reuters Finance
- TechCrunch
- CNBC Markets & Business
- Cointelegraph
- Bloomberg
