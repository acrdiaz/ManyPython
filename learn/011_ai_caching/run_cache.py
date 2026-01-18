import os

from google import genai
from google.genai import types
from google.generativeai import count_tokens


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "script.txt")

# Check Token Count
with open(file_path, "r") as f:
    print("Token count:", count_tokens(f.read()))


# # Initialize the client
# client = genai.Client()

# # 1. Upload the file (if required)
# document = client.files.upload(file=file_path)

# # 2. Define the model
# model_name = "gemini-1.5-flash-001"

# # 3. Create cached content (with proper structure)
# cache = client.caches.create(
#     model=model_name,
#     config=types.CreateCachedContentConfig(
#         contents=[document],
#         system_instruction="You are an expert analyzing transcripts.",
#     ),
# )
# print("Cache:", cache)
# print("Cache created:", cache.name)

# # 4. Generate a summary
# response = client.models.generate_content(
#     model=model_name,
#     contents="Please summarize this transcript",
#     config=types.GenerateContentConfig(cached_content=cache.name),
# )
# print("Summary:", response.text)