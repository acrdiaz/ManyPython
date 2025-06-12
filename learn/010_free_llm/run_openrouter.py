# requirements
#   pip install openai
# https://openrouter.ai/models?q=free

from openai import OpenAI

import os

MODEL_DEEPSEEK_R1 = "deepseek/deepseek-r1:free"
MODEL_LLAMA = "meta-llama/llama-3.3-8b-instruct:free"
MODEL_PHI = "microsoft/phi-4-reasoning:free" # a bit verbose, output reasoning
MODEL_DEEPSEEK_QWEN = "deepseek/deepseek-r1-distill-qwen-32b:free" # a bit verbose
MODEL_LLAMA_SCOUT = "meta-llama/llama-4-scout:free"
MODEL_QWEN_3 = "qwen/qwen3-235b-a22b:free" # a bit verbose
MODEL_NVIDIA_LLAMA = "nvidia/llama-3.3-nemotron-super-49b-v1:free"
MODEL_MISTRAL_AI = "mistralai/devstral-small:free" # a bit verbose


API_TOKEN = os.getenv('OPENROUTER_API_KEY')
MODEL_DEFAULT = MODEL_MISTRAL_AI

PROMPT_CONTEXT = "Provide simple answer."
PROMPT = "Capital of France?"
PROMPT_SHORT = f"{PROMPT_CONTEXT} {PROMPT}"
PROMPT_DEFAULT = PROMPT


client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_TOKEN)
response = client.chat.completions.create(
    model=MODEL_DEFAULT,
    messages=[{"role": "user", "content": PROMPT_DEFAULT}]
)

print (response.choices[0].message.content)