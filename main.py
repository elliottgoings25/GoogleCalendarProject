from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent 

app = FastAPI()

class Request(BaseModel):
    message: str

@app.post("/chat")
def chat(req: Request):
    result = run_agent(req.message)

    # If Gemini wants to call a function
    if result["action"] == "create_calendar_event":
        return {
            "response": "I can schedule that for you.",
            "data": result["args"]
        }

    # Otherwise just return text
    return {"response": result["text"]}