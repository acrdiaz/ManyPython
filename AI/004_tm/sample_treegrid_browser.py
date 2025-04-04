# pip install langchain-google-genai
# pip install browser-use
# pip install requests

import os
import sys
from pathlib import Path
import asyncio

from browser_use.agent.views import ActionResult
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext


# Append the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize the browser with the specified configuration
BROWSER = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
)

SUMMARY_LENGTH = 2  # sentences

def load_file(file_path):
    return load_content(file_path)

def load_files(file_prompt_path, file_addinf_path):
    return load_content(file_prompt_path), load_content(file_addinf_path)

def load_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

def select_llm(model_name):
    if model_name.lower() == 'chatgpt':
        return ChatOpenAI(
            model='gpt-4o-mini',
            timeout=100,
            temperature=0.0,
            # stop=None,
            # max_tokens=1500
            )
    elif model_name.lower() == 'gemini':
        return ChatGoogleGenerativeAI(
            model='gemini-2.0-flash', 
            api_key=os.getenv('GEMINI_API_KEY'),
            timeout=100,               # Maximum time to wait for a response (in seconds)
            temperature=0.0,           # Controls randomness; 0.0 for deterministic output
            # stop=None,                 # Stopping sequence for the model's output
            max_tokens=1500            # Maximum number of tokens in the generated response
            )
    else:
        raise ValueError(f"Unsupported model name: {model_name}")

async def run_agent(prompt, additional_information, context, llm):
    agent = Agent(
        task=prompt,
        message_context=additional_information,
        context=context,
        llm=llm,
        # planner_llm=ChatOpenAI(model='o3-mini'),
        browser=BROWSER,
        # retry_attempts=1  # Set to 1 retry attempt
        max_failures=1,               # Number of allowed consecutive failures
        retry_delay=5,                # Delay between retries in seconds
        use_vision=True,              # Enable visual understanding of the page
        max_actions_per_step=3,       # Limit actions per step to prevent overloading
        include_attributes=[          # Customize which attributes to consider
            'title', 'type', 'name', 
            'role', 'aria-label',
            'data-auto-node',       # Unique node identifier
            'data-auto-nodekey',    # Node key for identification
            'data-auto-nodetitle',  # Node title
            'aria-expanded',        # Expansion state
            'id',                   # Unique DOM id
            'class',                # CSS classes
            'data-auto-icon',       # Icon identifier
            'draggable',            # Drag state
            'data-auto-node__active', # Active state
            'data-auto-button',     # Button identifier
            'data-auto-contextualmenu', # Context menu identifier
            'data-auto-menu'        # Menu identifier
        ],
        validate_output=False,         # Enable output validation
        max_input_tokens=64000,       # Adjust token limit based on your model
        planner_interval=2            # Run planner every 2 steps
    )

    page_content = await agent.run()
    return page_content

async def get_summary(prompt, page_content, llm):
    # ensure the agent returned valid content
    if not page_content: #or not isinstance(page_content, str):
        raise ValueError("Agent returned invalid or empty content.")

    # generate a summary of the page content
    content_size = page_content.history[-1].result[-1].extracted_content[:10000]
    summary_prompt = prompt.format(summary_length=SUMMARY_LENGTH, content_size=content_size)

    print("Generating summary...")
    #summary_result = await llm.invoke(summary_prompt)  # Use invoke() instead of generate_content()
    summary_result = llm.invoke(summary_prompt)
    summary = summary_result.content.strip()
    return summary

async def main():
    try:
        cwd = os.getcwd()
        if '004_tm' not in cwd:
            os.chdir(Path(cwd).joinpath('AI/004_tm'))

        context = "This task involves navigating to a specific URL and counting visible nodes in a treeview without expanding any nodes."

        model_name = input("Enter the model name (ChatGPT or Gemini): ")
        llm = select_llm(model_name)

        prompt_scenatio = input("Pick a prompt (a: add object, b: get summary): ")

        if 'a' in prompt_scenatio:
            # prompt a -- add a Risk with a title
            # '102_get_treegrid_folder_display_kebab.txt' -- draft
            # Good
            prompt, additional_information = load_files('01_prompt_add_procedure.txt', 'additional_information_treegrid.txt')
            await run_agent(prompt, additional_information, context, llm)
        elif 'b' in prompt_scenatio:
            # prompt b -- provide summary from an exiting object
            # Good
            prompt, additional_information = load_files('02_prompt_extract_text.txt', 'additional_information_treegrid.txt')
            page_content = await run_agent(prompt, additional_information, context, llm)
            # --
            prompt = load_file('03_prompt_get_summary.txt')
            summary = await get_summary(prompt, page_content, llm)
            print("\nAI Summary:\n", summary)
        elif 'c' in prompt_scenatio:
            # prompt b -- provide summary from an exiting object
            # - Locate the treegrid element 'Access Control Enhancement'
            # Good
            prompt, additional_information = load_files('02_prompt_extract_text_b.txt', 'additional_information_treegrid.txt')
            page_content = await run_agent(prompt, additional_information, context, llm)
            # --
            prompt = load_file('03_prompt_get_summary.txt')
            summary = await get_summary(prompt, page_content, llm)
            print("\nAI Summary:\n", summary)

        # prompt c -- detect if a parent object status is expanded/collapsed # expand
        # Good
        # prompt, additional_information = load_files('04_prompt_get_status.txt', 'additional_information_treegrid.txt')
        # await run_agent(prompt, additional_information, context, llm)

        # # prompt d -- detect if object is expandable, and if it is expanded # expand
        # # Bad, hallucinating -- trying to scroll to the bottom of the page, since object not found
        # prompt, additional_information = load_files('05_is_object_expandable.txt', 'additional_information_treegrid.txt')
        # await run_agent(prompt, additional_information, context, llm)

        # prompt d -- list object with type # object type -- in progress has bug
        # Bad it identifies object by  title and not by html properties
        # prompt, additional_information = load_files('06_list_objects_by_type.txt', 'additional_information_treegrid.txt')
        # await run_agent(prompt, additional_information, context, llm)


    except (FileNotFoundError, ValueError) as e:
        print(e)
    
    finally:
        await BROWSER.close()

    input('Press Enter to close...')


if __name__ == '__main__':
    asyncio.run(main())