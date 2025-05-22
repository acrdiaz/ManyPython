from pathlib import Path


DR_API = "Hi, master"

# Service constants
DR_STATUS_LOG_INTERVAL = 10  # seconds
DR_QUEUE_TIMEOUT = 1.0  # seconds
DR_THREAD_JOIN_TIMEOUT = 5.0  # seconds
DR_POLLING_INTERVAL = 0.7  # seconds prevent CPU hogging


DR_BASE_PATH = Path(__file__).parent.parent.absolute()
DR_DB_FOLDER = "db"
DR_PROMPT_FILE = "dr_prompt.txt"

DR_PROMPT_FILE_PATH = DR_BASE_PATH / DR_DB_FOLDER / DR_PROMPT_FILE