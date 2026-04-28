from datetime import datetime, timedelta
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.event import Event
from llm import ask_gemini

#------------------------------------
# Parses user input to extract event details using the LLM
#------------------------------------
def parse_event(text: str) -> Event:
    try:
        # Get today's date for reference
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        
        prompt = f"""Extract event details from this text. Handle relative dates like "next Thursday", "tomorrow", "a week from now", etc.

Today is: {today.strftime('%A, %B %d, %Y')}
Tomorrow: {tomorrow.strftime('%Y-%m-%d')}
A week from now: {next_week.strftime('%Y-%m-%d')}

Text: {text}

Return this exact JSON structure (use ISO 8601 format):
{{
    "title": "event title",
    "description": "event description",
    "start": "2026-04-20T10:00:00",
    "end": "2026-04-20T11:00:00"
}}

Rules:
- If time isn't specified, assume 10:00 AM - 11:00 AM
- If only a date is given (no time), assume 10:00 AM start
- Handle phrases like: "next Thursday", "tomorrow", "a week later", "in 2 days", "next Monday", etc.
- Always return times in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- If no description, use empty string"""
        
        groq_response = ask_gemini(prompt)
        
        # Clean and parse JSON
        clean_json = groq_response.replace('```json', '').replace('```', '').strip()
        event_data = json.loads(clean_json)
        
        return Event(
            title=event_data['title'],
            description=event_data['description'],
            start=event_data['start'],
            end=event_data['end']
        )
    except Exception as e:
        print(f"Error parsing event: {e}")
        return Event(
            title="Event",
            description="",
            start="2026-04-20T10:00:00",
            end="2026-04-20T11:00:00"
        )