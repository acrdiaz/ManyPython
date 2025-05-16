from fastapi import FastAPI
from app.utils.dr_globals import DR_API

app = FastAPI()

@app.get("/")
async def root():
    return {"message": f"Welcome to the FastAPI application: {DR_API}"}