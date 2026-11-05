from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)

def chat(messages: list[dict], temperature: float = 0.2) -> str:
    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content