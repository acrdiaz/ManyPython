from app.services.dr_browser_agent import DRBrowserUseAgent
from app.services.dr_prompt_consumer import DRPromptConsumer
from app.services.dr_prompt_producer import DRPromptProducer
from app.utils.dr_globals import (
    DR_POLLING_INTERVAL,
    DR_STATUS_LOG_INTERVAL,
    DR_QUEUE_TIMEOUT, 
    DR_THREAD_JOIN_TIMEOUT
)
from app.utils.dr_utils_file import DRUtilsFile
from queue import Queue
from typing import Dict, Any, Optional, List, Callable

import asyncio
import logging
import queue
import threading
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PromptService')


class DRPromptService:
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
        self.queue = Queue()
        self.running = False
        self.worker_thread = None
        self.results = {}  # Store results by prompt_id
        self.processor = processor_func or self._default_processor
        # self._status_thread = None

        self.promptFile = DRUtilsFile()
        self.prompt_queue = Queue()
        self.producer = DRPromptProducer(self.prompt_queue, self.promptFile)
        self.consumer = DRPromptConsumer(self.prompt_queue, self)

        logger.info("DRPromptService initialized")

    def _default_processor(self, prompt: str, metadata: Dict[str, Any]) -> str:
        """Default prompt processor that just logs the prompt."""
        logger.info(f"Processing prompt: {prompt[:50]}...")
        logger.info(f"Metadata: {metadata}")

        # Using DRBrowserUseAgent from the separate file
        browserAgent = DRBrowserUseAgent(browser_name="edge") # AA1 global
        asyncio.run(browserAgent.main(prompt, metadata))

        # Use metadata in the response if available
        priority = metadata.get('priority', 'normal')
        source = metadata.get('source', 'unknown')

        return f"Processed: {prompt[:50]}... (Priority: {priority}, Source: {source})"

    async def _run_browser_agent(self, agent):
        """Run the browser agent and close the browser when done."""
        try:
            await agent.run()
        finally:
            await agent.browser.close()

    def _process_next_prompt(self):
        """Process the next prompt from the queue."""
        try:
            # Get a prompt from the queue with a timeout
            prompt_id, prompt_text, metadata = self.queue.get(timeout=DR_QUEUE_TIMEOUT)
            logger.info(f"Processing prompt ID: {prompt_id}")
            
            # Process the prompt and update result
            self._process_prompt_and_update_result(prompt_id, prompt_text, metadata)
            
            # Mark the task as done
            self.queue.task_done()
        except queue.Empty:
            # Queue is empty, continue waiting
            pass

    def _process_prompt_and_update_result(self, prompt_id, prompt_text, metadata):
        """Process a prompt and update its result."""
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

    def start(self):
        """Start the service."""
        if self.running:
            logger.warning("Service is already running")
            return
        
        self.running = True
        # self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        # self.worker_thread.start()
        # self._status_thread = threading.Thread(target=self._status_loop, daemon=True) AA1 i probably do not need this
        # self._status_thread.start()
        self.producer.start()
        self.consumer.start()
        logger.info("Service started")

    def stop(self):
        """Stop the service."""
        if not self.running:
            logger.warning("Service is not running")
            return
        
        logger.info("Stopping service...")
        self.running = False
        # if self.worker_thread:
        #     self.worker_thread.join(timeout=DR_THREAD_JOIN_TIMEOUT)
        # if self._status_thread:
        #     self._status_thread.join(timeout=DR_THREAD_JOIN_TIMEOUT)
        self.producer.stop()
        self.consumer.stop()
        self.producer.join(timeout=DR_THREAD_JOIN_TIMEOUT) # AA1 is this OK?
        self.consumer.join(timeout=DR_THREAD_JOIN_TIMEOUT)
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
        metadata = metadata or {}

        if not self.running:
            raise RuntimeError("Service is not running")
        
        prompt_id = f"prompt_{int(time.time() * 1000)}"
        self.results[prompt_id] = {
            "status": "queued",
            "queued_at": time.time(),
            "prompt": prompt_text,
            "metadata": metadata
        }
        
        self.queue.put((prompt_id, prompt_text, metadata))
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