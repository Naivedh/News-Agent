# AI News Agent

Automated daily news briefing for tech and financial markets.

## Setup

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Configure credentials:
```bash
cp .env.example .env
nano .env  # Fill in your API keys
```

3. Test it:
```bash
chmod +x test_run.sh
./test_run.sh
```

## Daily Automation

Add to crontab to run every morning at 8 AM:
```bash
crontab -e
```

Add this line:
```
0 8 * * * cd /home/shnaiv/AI-Agent && export $(cat .env | xargs) && /usr/bin/python3 news_agent.py >> /home/shnaiv/AI-Agent/logs.txt 2>&1
```

## What You Need

1. **Groq API Key** (free): https://console.groq.com
2. **Resend API Key** (free, 100 emails/day): https://resend.com/api-keys
   - Sign up at https://resend.com
   - Create API key
   - Use `onboarding@resend.dev` as FROM email

## News Sources

- WSJ Markets
- Reuters Finance
- TechCrunch
- The Verge
- CNBC
- Cointelegraph
