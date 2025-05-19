# run \
#   py run.py

import uvicorn
import signal
import sys
from app.services.dr_prompt_service import DRPromptService

def signal_handler(sig, frame):
    """Handle termination signals gracefully."""
    print("Shutting down...")
    sys.exit(0)

def main():
    # Start the background service
    service = DRPromptService()
    service.start()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Run the FastAPI application (this will block until the server stops)
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    finally:
        # Stop the service when the application stops
        print("Stopping service...")
        service.stop()

if __name__ == "__main__":
    main()