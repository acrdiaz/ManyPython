import asyncio
import logging
import os
import queue
import threading
import time
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dr_browser_use.browser_use_service import DRBrowserUseService
# from dr_browser_use.dr_browser_use_service import DRBrowserUseService
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from dr_browser_use.dr_browser_use_service import DRBrowserUseService
from typing import Dict, Any, Optional, List, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PromptService')

class PromptService:
    """
    A service that runs in the background and processes a queue of prompts.
    """
    
    def __init__(self, processor_func: Callable[[str, Dict[str, Any]], Any] = None):
        """
        Initialize the prompt service.
        
        Args:
            processor_func: Function to process prompts. Should accept (prompt_text, metadata)
                           If None, a default processor that just logs the prompt will be used.
        """
        self.queue = queue.Queue()
        self.running = False
        self.worker_thread = None
        self.results = {}  # Store results by prompt_id
        self.processor = processor_func or self._default_processor
        logger.info("PromptService initialized")
    
    def _default_processor(self, prompt: str, metadata: Dict[str, Any]) -> str:
        """Default prompt processor that just logs the prompt."""
        logger.info(f"Processing prompt: {prompt[:50]}...")
        logger.info(f"Metadata: {metadata}")
        
        # Simulate processing time
        # time.sleep(10)
        # prompt = "open https://www.wikipedia.org/"
        buService = DRBrowserUseService()
        asyncio.run(buService.main(prompt))
        
        # Use metadata in the response if available
        priority = metadata.get('priority', 'normal')
        source = metadata.get('source', 'unknown')
        
        return f"Processed: {prompt[:50]}... (Priority: {priority}, Source: {source})"
    
    def _worker(self):
        """Worker thread that processes prompts from the queue."""
        logger.info("Worker thread started")
        while self.running:
            try:
                # Get a prompt from the queue with a timeout
                prompt_id, prompt_text, metadata = self.queue.get(timeout=1.0)
                logger.info(f"Processing prompt ID: {prompt_id}")
                
                try:
                    # Process the prompt
                    result = self.processor(prompt_text, metadata)
                    status = "completed"
                except Exception as e:
                    logger.error(f"Error processing prompt {prompt_id}: {str(e)}")
                    result = str(e)
                    status = "error"
                
                # Store the result
                self.results[prompt_id] = {
                    "status": status,
                    "result": result,
                    "completed_at": time.time(),
                    "prompt": prompt_text,
                    "metadata": metadata
                }
                
                # Mark the task as done
                self.queue.task_done()
                
            except queue.Empty:
                # Queue is empty, continue waiting
                pass
            except Exception as e:
                logger.error(f"Unexpected error in worker thread: {str(e)}")
        
        logger.info("Worker thread stopped")
    
    def start(self):
        """Start the service."""
        if self.running:
            logger.warning("Service is already running")
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        logger.info("Service started")
    
    def stop(self):
        """Stop the service."""
        if not self.running:
            logger.warning("Service is not running")
            return
        
        logger.info("Stopping service...")
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)
        logger.info("Service stopped")
    
    def add_prompt(self, prompt_text: str, metadata: Dict[str, Any] = None) -> str:
        """
        Add a prompt to the queue.
        
        Args:
            prompt_text: The prompt text to process
            metadata: Additional metadata for the prompt
            
        Returns:
            prompt_id: A unique ID for the prompt
        """
        if not self.running:
            raise RuntimeError("Service is not running")
        
        prompt_id = f"prompt_{int(time.time() * 1000)}"
        self.results[prompt_id] = {
            "status": "queued",
            "queued_at": time.time(),
            "prompt": prompt_text,
            "metadata": metadata or {}
        }
        
        self.queue.put((prompt_id, prompt_text, metadata or {}))
        logger.info(f"Added prompt to queue with ID: {prompt_id}")
        return prompt_id
    
    def get_status(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a prompt.
        
        Args:
            prompt_id: The ID of the prompt
            
        Returns:
            A dictionary with the status information, or None if not found
        """
        return self.results.get(prompt_id)
    
    def get_queue_size(self) -> int:
        """Get the current size of the queue."""
        return self.queue.qsize()
    
    def get_all_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get the status of all prompts."""
        return self.results


# Example usage
if __name__ == "__main__":
    # Create and start the service
    service = PromptService()
    service.start()
    
    try:
        # Add some prompts to the queue
        prompt_ids = []
        for i in range(5):
            prompt_id = service.add_prompt(
                f"This is test prompt #{i}",
                {"priority": i, "source": "test"}
            )
            prompt_ids.append(prompt_id)
        
        # Wait for processing and check statuses
        time.sleep(1)
        print(f"Queue size: {service.get_queue_size()}")
        
        # Wait for all prompts to be processed
        time.sleep(10)
        
        # Print results
        for prompt_id in prompt_ids:
            status = service.get_status(prompt_id)
            print(f"Prompt {prompt_id}: {status['status']}")
            if status['status'] == 'completed':
                print(f"  Result: {status['result']}")
        
    finally:
        # Stop the service
        service.stop()