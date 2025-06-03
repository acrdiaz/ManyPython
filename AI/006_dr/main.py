import os
import asyncio

from browser_use.agent.views import ActionResult # AgentHistoryList
from browser_use import Agent # Controller # AA1
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


# Initialize configuration
BROWSER = Browser(
    config=BrowserConfig(
        # chrome_instance_path='C:\\Program Files (x86)\\Microsoft\\Edge\Application\\msedge.exe',
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
)
MAX_STEPS = 30
MAX_ACTIONS_PER_STEP=7

API_KEY = SecretStr(os.getenv("GEMINI_API_KEY"))
LLM_GEMINI = 'gemini-2.0-flash'
LLM_GPT = 'gpt-4o-mini'

DEFAULT_MODEL = 'g' # 'g' for Gemini, 'c' for ChatGPT


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
            temperature=0.0,
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

async def get_llm_response(prompt, llm):
    """Get direct response from LLM for simple knowledge queries."""
    try:
        prompt_llm = f"""
Prompt: {prompt}.
If the Prompt is a simple knowledge query, answer it.
If the Prompt looks like instructions to interact with a website, respond with 'NEEDS_BROWSER'.
        """
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
1. If you encounter a click error or cannot access an element:
1.1. Check if the information is available on the current page
1.2. Report what information you found and what's missing
    """
    combined_context = f"{additional_information or ''}.\n{error_recovery_context}"
    
    agent = Agent(
        task=prompt,
        message_context=combined_context,
        # planner_llm=planner_llm,
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
        max_actions_per_step=MAX_ACTIONS_PER_STEP,
        # validate_output=True,
        # max_input_tokens=64000,
        max_failures=2,                             # Increase max failures to allow for retries
        # retry_delay=1,                            # Short delay between retries
        # # enable_memory=True                      # Enable memory to remember failed attempts
        # tool_calling_method='function_calling'      # Add this line ....
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

def load_dr_prompt(user_action):
    match user_action:
        case 'a':
            task = """
1. Open the website dReveal.com
2. Click on the 'Try it for FREE' button to open the File manager
3. After page changes, describe in a sentence what do you see.
            """
            additional_information = """
.
            """
        case 'b':
            task = """
1. Open the Dashboards folder to list all available dashboards.
            """
            additional_information = """
1. Double Click may have challenges, ensure to try different click approaches, double click should do the work.
2. Use the double click on index: 21 or 22 or 23 it is the Folder icon
3. Should be completed in 5 steps maximum.
4. If you encounter a click error or cannot access an element, describe in a clean sentence what do you see.
            """
        case 'c':
            task = """
1. Please print a list of all the available dashboard files.
2. Also print the file sizes.
3. Tell me thte name and size of the largest file.
            """
            additional_information = """
1. Click on the first file to set the focus and vertical scroll will appear.
2. There is a vertical scroll class='dx-scrollable-content' scroll to load all the files
3. Display list in a numbered list format.
            """
        case 'd':
            task = """
1. Extract the data, make a executive summary report of the dashboard.
            """
            additional_information = """
.
            """
        case 'e':
            task = """
1. The dashboard: 'Select Chart Metric', has a cog menu, click on it to open the Options panel.
2. Maximize the dashboard.
            """
# 3. Perform a cusomization, Rotated is OFF, change it to ON, click the ON button.
            additional_information = """
1. The dashboard header has buttons: Export, Maximize, Cog Menu.
2. The Cog Menu is index: 21
3. The Menu code is: <div role="button" class="dx-widget dx-button dx-button-mode-contained dx-button-normal" tabindex="0" title="Menu">
            """
        case 'f':
            task = """
1. Perform the export to image Pro, in PNG format.
2. Use the Export button.
            """
            additional_information = """
1. Top right corner has the Actions button, click on it to open the export menu.
2. There are no notification, the user should verify the export.
            """
        case _:
            task = "Unknown"
            additional_information = None

    return (
        task,
        additional_information
    )

async def main():
    print("\n=== AI Select a dReveal Action ===")
    print("a. Open File manager")
    print("b. Open Dashboards folder -- under construction")
    print("c. Make a list of all available dashboards")
    print("d. Sales Performance Analysis.dDashX -- summorize dashboard content")
    print("e. Sales Performance Analysis.dDashX -- Custom Dashview -- under construction")
    print("f. Sales Performance Analysis.dDashX -- Export to Excel")
    print("q. Quit\n")
    
    user_action = input("Select action or 'q' to quit: ").lower()
    
    if user_action == 'q':
        return
        
    if len(user_action) != 1 or user_action < 'a' or user_action > 'f':
        print("Invalid choice. Please select an action.")
        return
        
    model_instance = get_model_instance(DEFAULT_MODEL)
    if not model_instance:
        print("Error initializing the model. Please try again.")
        return
    
    model_planner = get_model_instance(DEFAULT_MODEL)
    if not model_planner:
        print("Error initializing the model planner. Please try again.")
        return


    prompt, additional_information = load_dr_prompt(user_action)
    
    print(f"\n🚀 Action:\n{prompt}")
    # print(f"\n🚀 Context:\n{additional_information}\n")
    input("Press Enter to begin...")

    page_content = await run_agent(
        prompt=prompt,
        additional_information=additional_information,
        planner_llm=model_planner,
        llm=model_instance
    )
    
    success, status_message, final_answer, needs_help = evaluate_agent_response(page_content)
    
    if needs_help:
        assistance, action_type = await get_user_assistance(status_message)
        
        if action_type == "abort":
            print("Task aborted by user")
            return
        elif action_type == "skip":
            print("Skipping current step...")
            return
        elif assistance:
            # Update the prompt with user assistance
            if action_type == "search":
                additional_information = f"Try searching for: {assistance}"
            else:
                additional_information = f"Try this navigation path: {assistance}"
            return
        
    if success and final_answer:
        print("\n✅ Success!")
        print("Answer:", final_answer)
        return
    else:
        # raise Exception("Failed to extract answer from response") # pylint: disable=W0718 # AA1 delete
        print("\n❌ Failed to extract answer from response")


if __name__ == "__main__":
    try:
        asyncio.run(main())

        print('\n'.join([''] * 3))
        input("Press Enter to close the program...")
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        print(f"Good bye.")