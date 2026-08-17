from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate(system_prompt: str, user_message: str, history: list = []) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    messages += history
    messages.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, max_tokens=300, temperature=0.7)
    return response.choices[0].message.content