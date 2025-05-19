from app.utils.dr_globals import DR_API

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers when you create them
# from app.api.example_router import router as example_router


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Register routers
# app.include_router(example_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to the FastAPI application: {DR_API}"}

# @app.post("/prompt/") ...................
# async def create_prompt(prompt: str):
#     if get_prompt_file_size() == 0:
#         write_prompt_file(prompt)
#         return {"message": "Prompt created successfully!", "prompt": prompt}
#     else:
#         return {"message": "Try again later, a prompt is in queue."}