# run from \ManyPython
#   uvicorn AI.007_FastAPI.main_api:app --reload
# pip install fastapi-cors

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
# from .base.dr_web_auto import DRWebAuto


PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.txt")
app = FastAPI()

def get_prompt_file_size():
    try:
        return os.path.getsize(PROMPT_PATH)
    except FileNotFoundError:
        print("prompt.txt file not found.")
        return 0

def write_prompt_file(prompt: str):
    try:
        with open(PROMPT_PATH, "w") as file:
            file.write(prompt)
    except FileNotFoundError:
        print("prompt.txt file not found.")
    except Exception as e:
        print(f"An error occurred while cleaning the prompt file: {e}")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application"}

@app.post("/prompt/")
async def create_prompt(prompt: str):
    if get_prompt_file_size() == 0:
        write_prompt_file(prompt)
        return {"message": "Prompt created successfully!", "prompt": prompt}
    else:
        return {"message": "Try again later, a prompt is in queue."}

@app.post("/")
async def clear_prompt():
    if get_prompt_file_size() > 0:
        write_prompt_file('')
        
    return {"message": "Prompt cleared successfully!"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "query": q}

# # Define a POST endpoint
# @app.post("/items/")
# def create_item(items: List[dict]):
#     return {"message": "Items created successfully!", "items": items}