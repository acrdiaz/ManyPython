import os
from mistralai import Mistral

API_TOKEN = os.environ["MISTRAL_API_KEY"]
MODEL = "codestral-latest"
PROMPT = "Write a function for fibonacci"

message = [{"role": "user", "content": PROMPT}]

client = Mistral(api_key=API_TOKEN)
chat_response = client.chat.complete(
    model=MODEL,
    messages=message
)

print(chat_response.choices[0].message.content)