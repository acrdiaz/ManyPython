import threading
import logging

from app.utils.dr_globals import DR_QUEUE_TIMEOUT


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
                prompt_id, prompt_text, metadata = self.queue.get(timeout=DR_QUEUE_TIMEOUT)
                self.queue.task_done()
            except Exception as e:
                logger.error(f"Error in consumer thread: {str(e)}")
