import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.event import Event
from llm import ask_llm

#-----------------------------
# Parser function that uses Groq to extract event details from text
#-----------------------------
def parse_event(text: str) -> Event:
    try:
        prompt = f"""Extract event details from this text. Return ONLY valid JSON with no markdown formatting.

Text: {text}

Return this exact JSON structure:
{{
    "title": "event title",
    "description": "event description",
    "start": "2026-04-20T10:00:00",
    "end": "2026-04-20T11:00:00"
}}

If i say next week, assume that means the earlies it could possibly be is the nearest sunday, but use the day of the week specified
If something is unspecified, kill the prompt."""
        
        # Call your existing Groq function
        groq_response = ask_llm(prompt)
        
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
        # Fallback to dummy event
        return Event(
            title="Event",
            description="",
            start="2026-04-20T10:00:00",
            end="2026-04-20T11:00:00"
        )