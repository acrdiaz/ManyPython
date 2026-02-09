# python.exe -m pip install --upgrade pip
# pip install -q -U google-generativeai
# pip install -q -U google-genai
# pip show google-generativeai
# pip show google-genai

# list of models
# https://ai.google.dev/gemini-api/docs/models

from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

model = "gemini-3-flash-preview"
#        gemini-3-pro-preview     # quota exceeded
#        gemini-3-flash-preview   # works
#        gemini-2.5-flash         # works
#        gemini-2.5-flash-lite    # works
#        gemini-2.5-pro           # quota exceeded
#        gemini-2.0-flash         # quota exceeded
prompt = "Hi, i think it is noon now. What do you think?"

response = client.models.generate_content(
    model=model,
    contents=prompt
)

print(response.text)
