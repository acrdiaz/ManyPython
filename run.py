# run \
#   py run.py

import uvicorn
from app.services.prompt_service import PromptService

def main():
    # Start the background service if needed
    service = PromptService()
    service.start()
    
    try:
        # Run the FastAPI application
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    finally:
        # Stop the service when the application stops
        service.stop()

if __name__ == "__main__":
    main()