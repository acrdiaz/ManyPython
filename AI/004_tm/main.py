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
        chrome_instance_path='C:\\Program Files (x86)\\Microsoft\\Edge\Application\\msedge.exe',
    )
)
MAX_STEPS = 30
MAX_ACTIONS_PER_STEP=7

API_KEY = SecretStr(os.getenv("GEMINI_API_KEY"))
LLM_GEMINI = 'gemini-2.0-flash'
LLM_GPT = 'gpt-4o-mini'

DEFAULT_MODEL = 'c'


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
        tool_calling_method='function_calling'      # Add this line
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
1. Open TeamMate website
2. Login with credentials: admin.--/password
3. After login, describe what you see on the page.
            """
            additional_information = """
1. use the URL https://rc-sample.wktmdev.com/TeamMate
2. the username credentials may have special characters do not remove them.
3. The description present in numbered format.
            """
        case 'b':
            task = """
1. Use the Get button and add Summary project widget.
            """
            additional_information = """
1. The Get button is top right area.
2. Get button will display a panel with a list of widgets.
3. Pick a widget by check on the checkbox,then use the Insert button.
4. Close the panel.
            """
        case 'c':
            task = """
1. The Summary project widget resize to 100%.
            """
            additional_information = """
1. Resize the widget use the resize button to display a panel of percentages.
2. AFter percentage is selected, Click OK to close the percentage panel.
            """
        case 'd':
            task = """
1. Get the version of the website.
2. An tell me if SignalR test is good.
3. Go back to home page.
            """
            additional_information = """
1. On the top right corner use the avatar to display the panel.
2. The panel has the Support page option, click on it.
3. Extract the Build Version and Date.
            """
        case 'e':
            task = """
1. Open the project 05: German - Translations.com
            """
            additional_information = """
1. Use the hamburger menu from the top left corner to display the menu.
2. Select project.
3. The List of projects will be displayed, use the search box to find the project.
4. The search box does not have a search button, just type in thet content.
4. Click on the project to open it use the Ribbon Open button.
            """
        case 'f':
            task = """
1. Add tp the 'Corporate Accounting' object. a new object 'Control'.
2. 'Control' with a custom title 'Demo B Control Wednesday'.
            """
            additional_information = """
1. No scrolling.
2. ignore top 'Add' menu button, only use second Add from tree grid.
3. Set Focus on 'Corporate Accounting' object.
4. Kebab menu (secondary menu) is on the row of the tree grid, click on 'Add' > 'Control'. After click on Control Wait 2 seconds.
5. Find the 'New' object, click on the >> to display the 'Form View' panel, set the custom title.
            """
        case 'g':
            task = """
1. The 'Form view' is a set of Fields for one object.
2. To the 'Notes' field type in this text: 'Note: This is a demo CONTROL created by AI. This text is inserted into athe HTML field by AI.'
            """
            additional_information = """
1. Next to The title, under the title is the text editor.
2. If there is existing text, append the text.
3. Finally, Close button is on the top right corner to close the 'Form View' panel.
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
    print("a. Login to TeamMate")
    print("b. Add a custom widget")
    print("c. Add a custom widget -- resize to 100%")
    print("d. Get the website version")
    print("e. Open the project 05: German - Translations.com")
    print("f. Add a 'Control' object")
    print("g. Add text to 'Control' object")
    print("q. Quit\n")
    
    user_action = input("Select action or 'q' to quit: ").lower()
    
    if user_action == 'q':
        return
        
    if len(user_action) != 1 or user_action < 'a' or user_action > 'g':
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
    print(f"\n🚀 Context:\n{additional_information}\n")
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