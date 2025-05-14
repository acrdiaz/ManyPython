import os
import time

from dr_service.prompt_service import PromptService


PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.txt")

def get_prompt_file_size():
    try:
        return os.path.getsize(PROMPT_PATH)
    except FileNotFoundError:
        print("prompt.txt file not found.")
        return 0

def load_prompt_file():
    try:
        if os.path.getsize(PROMPT_PATH) == 0:
            return None

        with open(PROMPT_PATH, "r") as file:
            prompt = file.read().strip()
            if prompt:
                return prompt
            else:
                return None
    except FileNotFoundError:
        print("prompt.txt file not found.")
        return None

def clean_prompt_file():
    try:
        with open(PROMPT_PATH, "w") as file:
            file.write("")
    except FileNotFoundError:
        print("prompt.txt file not found.")
    except Exception as e:
        print(f"An error occurred while cleaning the prompt file: {e}")

def main():
    print("Starting Prompt Service...")
    
    promptService = PromptService()
    promptService.start()
    
    print("Prompt Service is running in the background.")
    print("You can add prompts to the queue and check their status.")
    
    try:
        while True:
            if get_prompt_file_size() > 0:
                prompt_text = load_prompt_file()
                if prompt_text:
                    print(f"Loaded prompt: {prompt_text}")
                    clean_prompt_file()
                    priority = "Normal" or None

                    metadata = {}
                    if priority.strip():
                        try:
                            metadata['priority'] = int(priority)
                        except ValueError:
                            metadata['priority'] = priority
                    
                    prompt_id = promptService.add_prompt(prompt_text, metadata)
                # else:
                #     print("No valid prompt found in the file.")

            # Small delay to prevent CPU hogging
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nInterrupted by user. Shutting down...")
    finally:
        # Make sure to stop the service before exiting
        promptService.stop()
        print("Service stopped. Goodbye!")

if __name__ == "__main__":
    main()