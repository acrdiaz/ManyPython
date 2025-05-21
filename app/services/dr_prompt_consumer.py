import threading
import logging
import time

from app.utils.dr_globals import DR_POLLING_INTERVAL


logger = logging.getLogger('PromptService')

class DRPromptConsumer(threading.Thread):
    def __init__(self, queue, service):
        super().__init__()
        self.queue = queue
        self.service = service
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            try:
                prompt_id, prompt_text, metadata = self.queue.get()
                self.queue.task_done()

                # Small delay to prevent CPU hogging
                time.sleep(DR_POLLING_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in consumer thread: {str(e)}")
