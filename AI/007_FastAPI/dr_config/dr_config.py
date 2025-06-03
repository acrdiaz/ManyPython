from pathlib import Path

DR_BASE_PATH = Path(__file__).parent.parent.absolute()
DR_DB_FOLDER = "dr_db"
DR_PROMPT_FILE = "prompt.txt"

DR_PROMPT_FILE_PATH = DR_BASE_PATH / DR_DB_FOLDER / DR_PROMPT_FILE