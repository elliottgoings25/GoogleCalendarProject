import sys
from PyQt5.QtWidgets import QApplication
from ui.calendar_ui import CalendarUI
from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent 


#-----Main Code-----
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarUI()
    window.show()
    sys.exit(app.exec_())
    
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