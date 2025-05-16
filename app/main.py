from fastapi import FastAPI
from app.utils.dr_globals import DR_API
# Import routers when you create them
# from app.api.example_router import router as example_router

app = FastAPI()

# Register routers
# app.include_router(example_router)

@app.get("/")
async def root():
    return {"message": f"Welcome to the FastAPI application: {DR_API}"}