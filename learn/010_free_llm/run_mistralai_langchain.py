# https://docs.mistral.ai/getting-started/models/models_overview/

import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate 

API_TOKEN = os.environ["MISTRAL_API_KEY"]
MODEL_CODESTRAL = "codestral-latest"
MODEL_PIXTRAL = "pixtral-12b-2409"
MODEL_DEVSTRAL = "devstral-small-2505"
MODEL_DEFAULT = MODEL_DEVSTRAL

PROMPT = "Write a Python function for fibonacci"

message = [("user", PROMPT)]

llm = ChatMistralAI(model=MODEL_DEFAULT, temperature=0, api_key=API_TOKEN)
# llm.invoke([("user", "Write a function for fibonacci")])

# # Option 1: Simple invoke and print
# response = llm.invoke(PROMPT)
# print(response.content)

# Option 2: Using messages format (similar to the first example)
response = llm.invoke(message)
print(response.content)