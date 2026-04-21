from models.event import Event

#-------------------------
# ACTION: AI event parsing
#-------------------------
def parse_event(text: str) -> Event:
    # Temp hardcoded event
    return Event(
        title="test",
        description="testing",
        start="2026-04-23T09:00:00",
        end="2026-04-23T10:00:00"
    )