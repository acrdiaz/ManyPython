import os
import asyncio

from database import ContextListManager

from browser_use.agent.views import ActionResult # AgentHistoryList
from browser_use import Agent # Controller # AA1
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from utils import get_multiline_input

# Initialize configuration
BROWSER = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless=False,
        disable_security=False,
        # keep_alive=True,
        new_context_config=BrowserContextConfig(
            # keep_alive=True,
            disable_security=False,
        ),
    )
)
MAX_STEPS = 30

DB_CONTEXT = ContextListManager()

API_KEY = SecretStr(os.getenv("GEMINI_API_KEY"))
LLM_GEMINI = 'gemini-2.0-flash'
LLM_GPT = 'gpt-4o-mini-search-preview-2025-03-11' # 'gpt-4o-mini'

LLM_SELECTED = 'g'
LLM_PLANNER_SELECTED = 'c'


def get_model_instance(model_choice):
    """Returns the appropriate model instance based on user choice."""
    if model_choice == 'g':
        return ChatGoogleGenerativeAI(
            model=LLM_GEMINI,
            api_key=API_KEY,
            # timeout=100,
            temperature=0.0,
            max_tokens=32000
        )
    elif model_choice == 'c':
        return ChatOpenAI(
            model=LLM_GPT,
            # timeout=100,
            # temperature=0.0,
        )
    return None

async def initialize_browser():
    """Initialize or reinitialize the browser"""
    global BROWSER
    try:
        # First try to close existing browser if it exists
        try:
            if BROWSER:
                await BROWSER.close()
        except:
            pass
        
        # Initialize new browser instance
        BROWSER = Browser(
            config=BrowserConfig(
                chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            )
        )
        print("✅ Browser initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize browser: {e}")
        return False

async def process_user_prompt(prompt, llm):
    valid_key = False

    retry_count = 3

    while not valid_key and retry_count > 0:
        retry_count -= 1
        print("\nEvaluating the user prompt...")
        key = llm_evaluate_user_prompt(prompt, llm)
        await asyncio.sleep(1)
        additional_information = DB_CONTEXT.get_entry(key)

        print("\nEvaluating LLM response...")
        valid_key = evaluate_llm_response(prompt, key, llm)
        await asyncio.sleep(1)
        print(f"LLM response is {'valid' if valid_key else 'invalid'}")

    if retry_count == 0 and not valid_key:
        print("\n❌ Unable to evaluate the user prompt after multiple attempts.")
        print("Terminating the process...")
        exit(0)
    else:
        return key
    
    # # AA1 delete this
    # print(f"\nKey: {key}")
    # print(additional_information)
    # exit(0)

def llm_evaluate_user_prompt(prompt, llm):
    """Evaluate the prompt to determine the key for the database"""
    try:
        # AA1 Can this text be refactored to another file?
        prompt_llm = f"""
You are an expert user using dreveal this page: dreveal.com.
List of dictionary keys: {DB_CONTEXT.get_all_keys_comma_separated()}.
Match the most relevant key based on this prompt: "{prompt}".
If no key matches the prompt, respond with 'None'.
Respond with the matching key only, without any additional text.
If the prompt does not match the key, respond with 'None'.
        """
        response = llm.invoke(prompt_llm)
        if response:
            key = response.content.strip()
            return key
        else:
            raise ValueError("No response from LLM")
    except Exception as e:
        print(f"Error evaluating prompt: {e}")
        return None

def evaluate_llm_response(prompt, key, llm):
    valid = False
    """Evaluate the prompt to determine the key for the database"""
    try:
        prompt_llm = f"""
You are an expert auditor using and auditing software.
Is the following prompt relevant to the given context?
* prompt: {prompt}
* context: {key}
Respond True or False, without any additional text.
        """
        response = llm.invoke(prompt_llm)
        if response is not None and response.content: # AA1 and hasattr(response, 'content') 
            valid = response.content.strip()
            return valid.lower() == 'true'
        else:
            raise ValueError("No response from LLM")
    except Exception as e:
        print(f"Error evaluating prompt: {e}")
        return False

async def get_llm_response(question, llm):
    """Get direct response from LLM for simple knowledge queries."""
    try:
        prompt_llm = f"""
Prompt: {question}
If the Prompt is a simple knowledge query, answer it.
If the Prompt looks like instructions to interact with a website, respond with 'NEEDS_BROWSER'.
        """
        # Identify if the prompt is a question or instruction(s) to interact with a website.
        # If it is an instruction to interact with a website, respond with 'NEEDS_BROWSER'.
        # If it is an instruction or requires interaction with a website, respond with 'NEEDS_BROWSER'.
        # If it requires web browsing or complex interaction, respond with 'NEEDS_BROWSER'.
        response = llm.invoke(prompt_llm)
        answer = response.content.strip()
        return None if "NEEDS_BROWSER" in answer else answer
    except Exception as e:
        print(f"Error getting LLM response: {e}")
        return None

async def run_agent(
        prompt,
        additional_information,
        planner_llm,
        llm
):
    # Add context about error recovery
    error_recovery_context = """
    If you encounter a click error or cannot access an element:
    * Check if the information is available on the current page
    * Report what information you found and what's missing
    """
    # * Look for similar elements with different attributes
    # * Try alternative navigation paths
    # * Consider using search functionality if available
    
    combined_context = f"{additional_information or ''}\n{error_recovery_context}"
    
    agent = Agent(
        task=prompt,
        message_context=combined_context,
        planner_llm=planner_llm,
        # planner_interval=1,
        llm=llm,
        browser=BROWSER,
        # include_attributes=[
        #     'title', 'type', 'name', 'role',
        #     'aria-label', 'placeholder', 'value',
        #     'alt', 'aria-expanded', 'data-date-format',
        #     'href', 'id', 'class',
        #     'button', 'link', 'text',  # Add more interactive elements
        #     'data-testid', 'data-cy'   # Add more test identifiers
        # ],
        # use_vision=True,
        # use_vision_for_planner=True,
        # max_actions_per_step=3,                     # AA1 is this number arbitrary?
        # validate_output=True,
        # max_input_tokens=64000,
        max_failures=2,                             # Increase max failures to allow for retries
        retry_delay=3,                              # Short delay between retries
        # # enable_memory=True                      # Enable memory to remember failed attempts
        # tool_calling_method='function_calling'      # Add this line
    )

    page_content = await agent.run(max_steps=MAX_STEPS)  # Increase max steps to allow for recovery, 3 steps
    # page_content = await agent.run()
    return page_content

def evaluate_agent_response(page_content):
    """
    Evaluates if the agent successfully completed the task and handles user assistance.
    Returns (success, message, final_answer, needs_help)
    """
    try:
        if isinstance(page_content, ActionResult):
            if "Failed - I was not able to click" in str(page_content):
                return (
                    False,
                    "Needs assistance with navigation",
                    page_content.extracted_content,
                    True
                )
            return (
                page_content.success,
                "Direct result received",
                page_content.extracted_content,
                False
            )
        
        # Check if we have a history of results
        if hasattr(page_content, 'history'):
            last_result = page_content.history[-1].result[-1]
            last_result_content = page_content.final_result()
 
            if page_content.is_done() and page_content.is_successful():
                # print('✅')
                # print(f"Result: {last_result_content}")
                return (
                    last_result.success,                            # success
                    "Task completed successfully",                  # status_message
                    last_result_content,                            # final_answer -- last_result.extracted_content,
                    False                                           # needs_help
                )
            else:
                # print('❌')
                # print(f"Failed to get result: {last_result_content}")
                return (
                    last_result.success,                            # success
                    f"Need help: {last_result.extracted_content}",  # status_message
                    last_result_content,                            # final_answer -- last_result.extracted_content,
                    True                                            # needs_help
                )
            
        return False, "Unknown response format", None, False
        
    except Exception as e: # pylint: disable=W0718
        return False, f"Error processing response: {str(e)}", None, False

async def get_user_assistance(error_message):
    """Get assistance from user when agent is blocked"""
    print("\n🤔 Agent needs help!")
    print(f"Issue: {error_message}")
    print("\nOptions:")
    print("1. Provide alternative search terms")
    print("2. Suggest different navigation path")
    print("3. Skip this step")
    print("4. Abort task")
    
    choice = input("\nWhat would you like to do? (1-4): ")
    
    if choice == "1":
        return input("Enter alternative search terms: "), "search"
    elif choice == "2":
        return input("Describe the navigation path: "), "navigate"
    elif choice == "3":
        return None, "skip"
    else:
        return None, "abort"

async def handle_browser_error(e):
    """Helper function to handle browser-specific errors"""
    if ("Target page, context or browser has been closed" in str(e) or 
        "Browser is not initialized" in str(e)):
        print("\n❌ Browser connection lost. Attempting to reconnect...")
        return await initialize_browser()
    return False

async def cleanup():
    """Cleanup function to properly close browser and handle resources"""
    try:
        if BROWSER:
            await BROWSER.close()
    except Exception as e:
        print(f"Cleanup warning: {e}")

async def main(question=None):

    """
    # print("\n=== AI Model Interface ===")
    # print("g. Gemini")
    # print("c. ChatGPT")
    # print("q. Quit")
    
    # choice = input("Select model (g/c) or 'q' to quit: ").lower()
    
    # if choice == 'q':
    #     print("Goodbye!")
    #     break
        
    # if choice not in ['g', 'c']:
    #     print("Invalid choice. Please select 'g' or 'c'.")
    #     continue
        
    #  model_instance = get_model_instance(choice)
    """
    model_instance = get_model_instance(LLM_SELECTED)
    if not model_instance:
        print("Error initializing the model. Please try again.")
        # continue
        return
    
    model_planner = get_model_instance(LLM_PLANNER_SELECTED)
    if not model_planner:
        print("Error initializing the model planner. Please try again.")
        # continue
        return

    # D:\prj\github\ManyPython\\database.py
    result = DB_CONTEXT.load_database(path='AI\\004_tm')
    if not result:
        print("Error loading database. Please check the file path and format.")
        # continue
        return

    # once = True # AA1 delete
    # while once:
    # while True:
        # once = False
    
    if question is None: # AA1 delete this
        # while True:  # Inner loop for multiple questions with same model
        if True:  # AA1 delete this line
            question = get_multiline_input("Task Prompt", "Enter your task/prompt (or 'q' to quit):")
           
            if not question or question.lower() == 'q' or not question.strip():
                return

    if True: # AA1 delete this line
            max_retries = 300
            retry_count = 0
           
            try:
                # AA1 commented this temp
                # print("Processing your question...")
                # direct_answer = await get_llm_response(question, model_instance)
               
                # if direct_answer:
                #     print("\nAnswer from LLM:\n", direct_answer)
                #     # continue  # Allow next question
                #     return # AA1 temp code
                
                # key = await process_user_prompt(question, model_instance)

                # print(f"\n🟢 Key: {key}")

                # if key == 'None':
                #     print("\nThe task/prompt does not appear to belong to the Auditing domain.")
                #     print("Terminating the process...")
                #     exit(0)

                # additional_information = DB_CONTEXT.get_entry(key)
                additional_information = """
1. Customize_Dashboard
1.1. Buttons are <div> elements, has attribute role="button"
1.2. Use the menu option of the dashpoard to open customization panel
1.3. To customize colors use the Color Scheme option panel
1.4. To start editing a color, click on corresponding <div class="dx-dashboard-edit-color-icon" data-bind="click: editColor">
     to display the colo picker
2. Ensure all communication is precise not verbose
                """

                retry_count = 0
                while True: # AA1 retry_count < max_retries: # infinite retry loop
                    try:
                        print("\nUsing browser to find answer...")

                        print(f"\n🟢 prompt:\n{question}")
                        print(f"\n🟢 additional_information:\n{additional_information}")

                        page_content = await run_agent(
                            prompt=question,
                            additional_information=additional_information,
                            planner_llm=model_planner,
                            llm=model_instance
                        )
                       
                        success, status_message, final_answer, needs_help = evaluate_agent_response(page_content)
                       
                        if needs_help:
                            assistance, action_type = await get_user_assistance(status_message)
                           
                            if action_type == "abort":
                                print("Task aborted by user")
                                break
                            elif action_type == "skip":
                                print("Skipping current step...")
                                continue
                            elif assistance:
                                # Update the prompt with user assistance
                                if action_type == "search":
                                    additional_information = f"Try searching for: {assistance}"
                                else:
                                    additional_information = f"Try this navigation path: {assistance}"
                                continue

                        if success and final_answer:
                            print("\n✅ Success!")
                            print("Answer:", final_answer)
                            break  # Exit retry loop but continue for next question
                        else:
                            # raise Exception("Failed to extract answer from response") # pylint: disable=W0718 # AA1 delete
                            print("\n❌ Failed to extract answer from response")
                            retry_count += 1
                            print(f"\n❌ Attempt {retry_count}/{max_retries} failed")
                            print(f"Error: {str(e)}")  # Add this line to show the actual error
                           
                            if retry_count < max_retries:
                                retry = input(f"\nRetry? ({max_retries - retry_count} attempts remaining) (y/n): ").lower()
                                if retry != 'y':
                                    break
                            else:
                                print("\n❌ Maximum retry attempts reached")
                                break
 
                    except Exception as e:  # pylint: disable=W0718
                        print(f"Error: {str(e)}")
                           
            except Exception as e:  # pylint: disable=W0718
                print(f"\n❌ Fatal error: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())

        print('\n'.join([''] * 3))
        input("Press Enter to close the program...")
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        print(f"Good bye.")