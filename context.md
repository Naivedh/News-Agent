# AI News Agent - Context & Documentation

## Project Overview
Automated daily news briefing system that fetches tech and financial news, analyzes it with AI, and emails a summary every morning.

## Architecture

### Components
1. **News Fetcher** - Pulls from 8 RSS feeds (WSJ Markets, WSJ Business, Reuters, TechCrunch, CNBC, CNBC Business, Cointelegraph, Bloomberg)
2. **AI Analyzer** - Uses Groq API (Llama 3.3 70B) to rank and summarize top 7-10 market-moving stories
3. **Email Sender** - Sends via Resend API with HTML formatting (bold labels, styled layout, blue borders)

### Tech Stack
- Python 3
- Libraries: `requests`, `feedparser`
- APIs: Groq (LLM), Resend (email)
- Scheduler: cron

## File Structure
```
/home/shnaiv/AI-Agent/
├── news_agent.py       # Main script
├── requirements.txt    # Python dependencies
├── .env               # API keys (DO NOT COMMIT)
├── .env.example       # Template for .env
├── test_run.sh        # Manual test script
├── README.md          # User documentation
└── context.md         # This file
```

## Configuration (.env)
```
GROQ_API_KEY=gsk_...           # From console.groq.com
RESEND_API_KEY=re_...          # From resend.com/api-keys
FROM_EMAIL=onboarding@resend.dev
RECIPIENT_EMAIL=user@email.com
```

## How It Works

1. **load_env()** - Reads .env file, parses KEY=value pairs, skips comments
2. **fetch_news()** - Fetches ~10 articles from each of 8 RSS feeds (~60-80 total)
3. **analyze()** - Sends articles to Groq API (Llama 3.3 70B) with prompt to select top 7-10 market-impacting stories with specific tickers and directions. Output format: numbered stories with clean spacing, stock chart emojis (📈 bullish, 📉 bearish), visual separators
4. **send_email()** - Formats content with HTML (bold labels, professional styling, blue borders) and sends via Resend API
5. **run()** - Orchestrates the flow

## API Usage & Limits

### Groq (Free Tier)
- Limit: 6,000 tokens per minute (TPM)
- Usage: 1 request/day
- Model: llama-3.3-70b-versatile (70B parameters)
- Temperature: 0.3 (focused, less creative)
- Context window: 131,072 tokens

### Resend (Free Tier)
- Limit: 100 emails/day
- Usage: 1 email/day
- From: onboarding@resend.dev (test domain)

### RSS Feeds (Free, Unlimited)
- No API keys needed
- No rate limits
- Public feeds

## News Sources
1. WSJ Markets - https://feeds.a.dj.com/rss/RSSMarketsMain.xml
2. WSJ Business - https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml
3. Reuters Finance - https://www.reuters.com/finance
4. TechCrunch - https://techcrunch.com/feed/
5. CNBC Markets - https://www.cnbc.com/id/100003114/device/rss/rss.html
6. CNBC Business - https://www.cnbc.com/id/10001147/device/rss/rss.html
7. Cointelegraph - https://cointelegraph.com/rss
8. Bloomberg - https://www.bloomberg.com/feed/podcast/etf-report.xml

## Automation Setup

### Cron Job (Daily at 8 AM)
```bash
crontab -e
```
Add:
```
0 8 * * * cd /home/shnaiv/AI-Agent && /usr/bin/python3 news_agent.py >> /home/shnaiv/AI-Agent/logs.txt 2>&1
```

### Manual Test
```bash
cd /home/shnaiv/AI-Agent
./test_run.sh
```

## Common Issues & Solutions

### Issue: "API key is invalid" (Resend)
- Check .env has `RESEND_API_KEY=re_...` (no spaces, no quotes)
- Regenerate key at resend.com/api-keys

### Issue: "KeyError: 'choices'" (Groq)
- Check .env has valid `GROQ_API_KEY=gsk_...`
- Verify key at console.groq.com

### Issue: Environment variables not loading
- Ensure .env has no extra spaces around `=`
- Comments must start with `#`
- The script has `load_env()` function that handles this

### Issue: Email not received
- Check spam folder
- Verify RECIPIENT_EMAIL in .env matches your Resend account email (e.g., shnaiv@amazon.com)
- With test domain (onboarding@resend.dev), you can ONLY send to your own verified email
- To send to other emails, verify a custom domain at resend.com/domains
- Check Resend dashboard for delivery status

## Future Enhancements (Ideas)

1. **More Sources**: Add Financial Times, Economist RSS feeds
2. **Filtering**: Skip articles older than 24 hours
3. **Sentiment Analysis**: Add bullish/bearish indicators per stock
4. **Stock Mentions**: Extract ticker symbols automatically
5. **HTML Email**: Better formatting with links and styling
6. **Slack/Discord**: Alternative to email
7. **Custom Schedule**: Different times for different days
8. **Error Notifications**: Alert if script fails
9. **Full Article Fetching**: Scrape full article text for more detailed analysis with specific numbers (EPS, revenue)
10. **Custom Domain**: Verify domain on Resend to send to any email address

## Maintenance Notes

- RSS feed URLs may change - check if articles stop coming
- Groq model: currently using llama-3.3-70b-versatile (upgraded from llama-3.1-8b-instant for better analysis)
- Groq rate limit: 6,000 tokens per minute - if hit, reduce articles per feed or summary length
- Resend test domain (onboarding@resend.dev) can only send to your verified email - verify custom domain for other recipients
- Check logs.txt periodically for errors
- Model analyzes ~60-80 articles and selects top 7-10 based on market impact

## Cost Breakdown
- Total: **$0/month**
- All services on free tier
- No credit card required

## Last Updated
2026-02-14
