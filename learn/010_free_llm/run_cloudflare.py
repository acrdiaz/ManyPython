"""
curl "https://api.cloudflare.com/client/v4/user/tokens/verify" ^
-H "Authorization: Bearer API_TOKEN"

# {"result":{"id":"fb44fb0b3ff891ff3759c4375228a0ae","status":"active"},"success":true,"errors":[],"messages":[{"code":10000,"message":"This API Token is valid and active","type":null}]}
"""
"""
curl  https://api.cloudflare.com/client/v4/accounts/53d1e4ee79403e5b5690ec302de94bda/ai/run/@cf/meta/llama-3-8b-instruct -H "Authorization: Bearer API_TOKEN" ^
  -d '{\"messages\":[{\"role\":\"system\",\"content\":\"You are a friendly assistant that helps write stories\"},{\"role\":\"user\",\"content\":\"Write a short story about a llama that goes on a journey to find an orange cloud \"}]}'

fix format...
"""

import os
import requests


API_TOKEN = os.getenv('CLOUDFLARE_API_KEY')
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/53d1e4ee79403e5b5690ec302de94bda/ai/run/"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


inputs = [
    { "role": "system", "content": "You are a database assistant that answers questions" },
    { "role": "user", "content": "capital of France"}
];
output = run("@cf/meta/llama-3-8b-instruct", inputs)
print(output)