import json
from models.event import Event
from services.gemini import parse_event_with_gemini

#------------------------------
# AI parsing of the event details
#------------------------------
def parse_event(text: str) -> Event:
    """Parse event from text using Gemini"""
    try:
        # Get JSON from Gemini
        gemini_response = parse_event_with_gemini(text)
        
        # Clean and parse JSON
        clean_json = gemini_response.replace('```json', '').replace('```', '').strip()
        event_data = json.loads(clean_json)
        
        return Event(
            title=event_data['title'],
            description=event_data['description'],
            start=event_data['start'],
            end=event_data['end']
        )
    #------------------------------
    # If parsing fails, return a default event will show
    #------------------------------
    except Exception as e:
        print(f"Error parsing event: {e}")
        return Event(
            title="Event",
            description="",
            start="2026-04-20T10:00:00",
            end="2026-04-20T11:00:00"
        )