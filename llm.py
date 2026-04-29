import os
from groq import Groq

def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing")

    return Groq(api_key=api_key)


# Actually grok not gemini, but it is the same thing
def ask_gemini(prompt):
    client = get_client()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content