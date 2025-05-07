# run from \ManyPython
#   uvicorn AI.007_FastAPI.main:app --reload

from fastapi import FastAPI
from typing import List
from .base.dr_web_auto import DRWebAuto

app = FastAPI()

LLM_GEMINI = 'gemini-2.0-flash'
LLM_GPT = 'gpt-4o-mini'

DEFAULT_MODEL = LLM_GEMINI

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application"}

@app.get("/open")
async def open_dr(prompt):
    browser = DRWebAuto()
    page_content = await browser.run_agent(
        llm=DEFAULT_MODEL,
        prompt=prompt,
    )

    if hasattr(page_content, 'history'):
        last_result = page_content.history[-1].result[-1]
        last_result_content = page_content.final_result()
        
        if page_content.is_done() and page_content.is_successful():
            result = last_result_content
        else:
            # result = page_content.get_result()
            # if not result:
            #     result = "No result found"
            # else:
            #     result = f"Need help: {last_result.extracted_content}"
            result = f"Need help: {last_result.extracted_content}"

    return {"message": result}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# Define a POST endpoint
@app.post("/items/")
def create_item(items: List[dict]):
    return {"message": "Items created successfully!", "items": items}