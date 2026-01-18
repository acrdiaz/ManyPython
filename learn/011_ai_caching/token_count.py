from google import genai

client = genai.Client()
prompt = "The quick brown fox jumps over the lazy dog."

# Count tokens using the new client method.
total_tokens = client.models.count_tokens(
    model="gemini-2.0-flash", contents=prompt
)
print("total_tokens: ", total_tokens)
# ( e.g., total_tokens: 10 )

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

# The usage_metadata provides detailed token counts.
print("usage_metadata: ",response.usage_metadata)
# ( e.g., prompt_token_count: 11, candidates_token_count: 73, total_token_count: 84 )