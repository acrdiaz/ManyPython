import threading
import logging
import queue
import time

from app.core.dr_globals import DR_POLLING_INTERVAL


logger = logging.getLogger('PromptService')

class DRPromptProducer(threading.Thread):
    def __init__(self, queue, prompt_file):
        super().__init__()
        self.queue = queue
        self.promptFile = prompt_file
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            try:
                if self.promptFile.dr_utils_get_prompt_file_size() == 0:
                    continue

                prompt_text = self.promptFile.dr_utils_load_prompt_file()
                if not prompt_text.strip():
                    continue

                logger.info(f"Loaded prompt: {prompt_text}")
                self.promptFile.dr_utils_clean_prompt_file()
                
                metadata = {'priority': 'Normal'}
                prompt_id = f"prompt_{int(time.time() * 1000)}"

                self.queue.put((prompt_id, prompt_text, metadata))
                
                # Small delay to prevent CPU hogging
                time.sleep(DR_POLLING_INTERVAL)

                print("producer...........")

            except Exception as e:
                logger.error(f"Error in producer thread: {str(e)}")