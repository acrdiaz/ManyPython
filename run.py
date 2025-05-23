# run \
#   py run.py

import uvicorn
from app.core.dr_globals import DR_PROMPT_FILE_PATH
from app.services.dr_prompt_service import DRPromptService
from app.utils.dr_utils_file import DRUtilsFile


def main():
    service = DRPromptService()

    try:
        service.start()

        uvicorn.run(
            "app.main:app", 
            host="127.0.0.1", 
            port=8000, 
            reload=True
        )

    finally:
        service.stop()

if __name__ == "__main__":
    main()