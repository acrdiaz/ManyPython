# run from \dr-ai-demos
#   uvicorn browser_use.Web_v_1_0.main:app --reload

from fastapi import FastAPI
from typing import List
# from src.dr_web_automate import DRWebAutomate

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application"}

# @app.get("/")
# async def Open_dReveal():
#     browser = DRWebAutomate("Chrome")
#     browser.open_url("http://localhost:8000/docs")
#     browser.close_browser()
#     return {"message": "Opening dReveal in the browser"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# Define a POST endpoint
@app.post("/items/")
def create_item(items: List[dict]):
    return {"message": "Items created successfully!", "items": items}