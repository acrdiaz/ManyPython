# python.exe -m pip install --upgrade pip
# pip install -q -U google-generativeai
# pip install -q -U google-genai
# pip show google-generativeai
# pip show google-genai

# list of models
# https://ai.google.dev/gemini-api/docs/model

from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

model = "gemini-2.0-flash"
prompt = "Hi, i think it is noon now. What do you think?"

response = client.models.generate_content(
    model=model, 
    contents=prompt
)

print(response.text)