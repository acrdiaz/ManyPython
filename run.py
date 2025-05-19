# run \
#   py run.py

import uvicorn
import threading
import time
import signal
import sys
from app.services.dr_prompt_service import DRPromptService

def keep_service_running(service):
    """
    Function to keep the service running in a separate thread.
    Periodically checks service status and logs information.
    """
    try:
        while True:
            # Log service status or perform maintenance tasks
            queue_size = service.get_queue_size()
            print(f"Service is running. Current queue size: {queue_size}")
            time.sleep(60)  # Check every minute
    except Exception as e:
        print(f"Error in service monitoring thread: {e}")

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
        # Start a monitoring thread for the service
        monitor_thread = threading.Thread(
            target=keep_service_running,
            args=(service,),
            daemon=True  # This ensures the thread exits when the main program exits
        )
        monitor_thread.start()
        
        # Run the FastAPI application (this will block until the server stops)
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
        
    finally:
        # Stop the service when the application stops
        print("Stopping service...")
        service.stop()

if __name__ == "__main__":
    main()