#!/bin/bash
# Test script to run the news agent manually

cd /home/shnaiv/AI-Agent

# Load environment variables
export $(cat .env | xargs)

# Run the agent
python3 news_agent.py
