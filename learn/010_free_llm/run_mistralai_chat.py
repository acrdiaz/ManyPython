# https://docs.mistral.ai/getting-started/models/models_overview/

import os
from mistralai import Mistral

API_TOKEN = os.environ["MISTRAL_API_KEY"]
MODEL_CODESTRAL = "codestral-latest"
MODEL_PIXTRAL = "pixtral-12b-2409"
MODEL_DEVSTRAL = "devstral-small-2505"
MODEL_DEFAULT = MODEL_DEVSTRAL

PROMPT = "Write a function for fibonacci"

message = [{"role": "user", "content": PROMPT}]

client = Mistral(api_key=API_TOKEN)
chat_response = client.chat.complete(
    model=MODEL_DEFAULT,
    messages=message
)

print(chat_response.choices[0].message.content)