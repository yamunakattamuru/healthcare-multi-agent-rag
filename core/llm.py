import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


GROQ_MODEL = "openai/gpt-oss-120b"


def call_llm(system_prompt, user_prompt):
    """Send a request to Groq and return the response."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError("GROQ_API_KEY is missing.")

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.2,
            max_tokens=1500,
        )

        return response.choices[0].message.content.strip()

    except Exception as exc:
        print(f"Groq API error: {exc}")

        return (
            "I could not generate a response because the LLM request failed. "
            "Please check your Groq API key and connectivity."
        )