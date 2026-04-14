from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    message: str

@app.post("/chat")
def chat(req: Request):
    return {"response": f"You said: {req.message}"}