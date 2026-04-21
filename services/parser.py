from models.event import Event

# will eventually be where the ai code is added, currently has test data

def parse_event(text: str) -> Event:
    """
    Convert user input into structured event data.
    Replace this later with AI parsing.
    """

    # TEMP mock logic
    return Event(
        title="test",
        description="testing",
        start="2026-04-23T09:00:00",
        end="2026-04-23T10:00:00"
    )