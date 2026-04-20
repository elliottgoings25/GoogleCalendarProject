import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def run_agent(user_input: str):
    response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=user_input
)

    return {
        "response": response.text
    }