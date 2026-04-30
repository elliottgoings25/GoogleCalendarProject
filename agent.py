import os
import json
from dotenv import load_dotenv
from llm import ask_llm
from calendar import post_event

load_dotenv()

def run_agent(user_input: str):
    system_prompt = """You are a calendar assistant.
    If the user wants to schedule, create, or add an event, respond ONLY with JSON like this:
    {"action": "create_event", "title": "event title", "date": "YYYY-MM-DD", "start_time": "HH:MM", "end_time": "HH:MM", "description": ""}
    
    If it is NOT a scheduling request, respond normally as plain text.
    Do not include any extra text or explanation when returning JSON."""

    reply = ask_llm(user_input, system_prompt=system_prompt).strip()

    try:
        data = json.loads(reply)
        if data.get("action") == "create_event":
            start = f"{data['date']}T{data['start_time']}:00"
            end = f"{data['date']}T{data['end_time']}:00"
            post_event(
                summary=data["title"],
                start_datetime=start,
                end_datetime=end,
                description=data.get("description", "")
            )
            return {"response": f"Done! I've added '{data['title']}' to your calendar on {data['date']}."}
    except (json.JSONDecodeError, KeyError):
        pass

    return {"response": reply}