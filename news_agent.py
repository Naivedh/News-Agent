#!/usr/bin/env python3
import os
import json
from datetime import datetime
import requests
import feedparser

def load_env():
    """Load environment variables from .env file if it exists (for local testing)"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Only set if not already in environment (GitHub Secrets take priority)
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value.strip()

class NewsAgent:
    def __init__(self):
        load_env()
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.resend_api_key = os.getenv('RESEND_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL')
        self.recipient = os.getenv('RECIPIENT_EMAIL')
        
        # Validate required keys
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env")
        if not self.resend_api_key:
            raise ValueError("RESEND_API_KEY not found in .env")
        if not self.from_email:
            raise ValueError("FROM_EMAIL not found in .env")
        if not self.recipient:
            raise ValueError("RECIPIENT_EMAIL not found in .env")
        
    def fetch_news(self):
        feeds = {
            'https://feeds.a.dj.com/rss/RSSMarketsMain.xml': 'WSJ Markets',
            'https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml': 'WSJ Business',
            'https://www.reuters.com/finance': 'Reuters Finance',
            'https://techcrunch.com/feed/': 'TechCrunch',
            'https://www.cnbc.com/id/100003114/device/rss/rss.html': 'CNBC',
            'https://www.cnbc.com/id/10001147/device/rss/rss.html': 'CNBC Business',
            'https://cointelegraph.com/rss': 'Cointelegraph',
            'https://www.bloomberg.com/feed/podcast/etf-report.xml': 'Bloomberg',
        }
        
        articles = []
        for url, source in feeds.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]:  # 10 per feed for better selection
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'source': source,
                        'summary': entry.get('summary', entry.get('description', ''))[:250]
                    })
            except Exception as e:
                print(f"Error {source}: {e}")
        
        return articles
    
    def analyze(self, articles):
        prompt = f"""You are a financial analyst. From these {len(articles)} news articles, select the top 7-10 that will MOST LIKELY move stock prices today.

STRICT RULES:
- ONLY publicly traded US companies with REAL ticker symbols (verify they exist)
- Focus on material events: earnings surprises, M&A, FDA approvals, major contracts, regulatory fines
- SKIP: private companies (Figure, ByteDance), opinion pieces, minor updates, political news without clear stock impact
- Extract specific numbers from summaries when available
- If a story affects MULTIPLE stocks, list ALL of them with their individual directions
- Use 📈 for Bullish and 📉 for Bearish

Articles: {json.dumps(articles, indent=2)}

Format (number each story, add blank line after each field):

1. [Title] ([Source])

Summary: [Key details from summary - include numbers if available]

Market Impact: [Specific reason why this moves stock prices]

Stocks: [TICKER1] 📈 Bullish, [TICKER2] 📉 Bearish - [Sector]

Link: [url]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': f'Bearer {self.groq_api_key}'},
            json={
                'model': 'llama-3.3-70b-versatile',  # Upgraded from llama-3.1-8b-instant
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.3,
                'max_tokens': 2000
            }
        )
        
        result = response.json()
        if 'choices' not in result:
            print(f"API Error: {result}")
            raise ValueError(f"Groq API error: {result.get('error', 'Unknown error')}")
        
        return result['choices'][0]['message']['content']
    
    def send_email(self, content):
        # Make labels bold
        content = content.replace('Summary:', '<strong>Summary:</strong>')
        content = content.replace('Market Impact:', '<strong>Market Impact:</strong>')
        content = content.replace('Stocks:', '<strong>Stocks:</strong>')
        content = content.replace('Link:', '<strong>Link:</strong>')
        content = content.replace('Source:', '<strong>Source:</strong>')
        
        # Convert plain text to HTML
        html_content = content.replace('\n\n', '<br><br>').replace('\n', '<br>')
        
        data = {
            'from': self.from_email,
            'to': [self.recipient],
            'subject': f"📊 Market News Briefing - {datetime.now().strftime('%b %d, %Y')}",
            'html': f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .story {{ margin-bottom: 30px; padding: 15px; background: #f8f9fa; border-left: 4px solid #3498db; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
        a {{ color: #3498db; text-decoration: none; }}
    </style>
</head>
<body>
    <h2>Good morning! 🌅</h2>
    <p>Here are today's top market-moving stories:</p>
    <div class="story">
        {html_content}
    </div>
    <div class="footer">
        Automated by AI News Agent
    </div>
</body>
</html>
"""
        }
        
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {self.resend_api_key}',
                'Content-Type': 'application/json'
            },
            json=data
        )
        
        if response.status_code == 200:
            print(f"✓ Email sent successfully")
        else:
            print(f"✗ Email failed: {response.status_code} - {response.text}")
    
    def run(self):
        print(f"[{datetime.now()}] Starting...")
        articles = self.fetch_news()
        print(f"✓ Fetched {len(articles)} articles")
        
        analysis = self.analyze(articles)
        print(f"✓ Analysis done\n")
        
        # Print output for review
        # print("="*80)
        # print("EMAIL PREVIEW:")
        # print("="*80)
        # print(f"Subject: 📊 Market News Briefing - {datetime.now().strftime('%b %d, %Y')}\n")
        # print("Good morning,\n")
        # print("Here are today's top market-moving stories:\n")
        # print(analysis)
        # print("\n---")
        # print("Automated by AI News Agent")
        # print("="*80)
        
        self.send_email(analysis)
        print("✓ Email sent")

if __name__ == '__main__':
    NewsAgent().run()
