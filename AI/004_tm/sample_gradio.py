import asyncio
import os
from dataclasses import dataclass
from typing import List, Optional

# Third-party imports
import gradio as gr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Local module imports
from browser_use import Agent, Browser, BrowserConfig

load_dotenv()


DEFAULT_LLM = 'gemini-2.0-flash'
DEFAULT_PROMPT = 'What is todays date'
DEFAULT_ADD_INFO = """
* use only www.yahoo.com
* do not use google.com
* Result in Spanish
"""

@dataclass
class ActionResult:
    is_done: bool
    extracted_content: Optional[str]
    error: Optional[str]
    include_in_memory: bool


@dataclass
class AgentHistoryList:
    all_results: List[ActionResult]
    all_model_outputs: List[dict]


def select_llm(model_name, api_key):
    if 'chatgpt' in model_name.lower():
        return ChatOpenAI(
            model='gpt-4o-mini',
            timeout=100,               # Maximum time to wait for a response (in seconds)
            temperature=0.0,           # Controls randomness; 0.0 for deterministic output
            stop=None,                 # Stopping sequence for the model's output
            max_tokens=1500            # Maximum number of tokens in the generated response
        )
    elif 'gemini' in model_name.lower():
        return ChatGoogleGenerativeAI(
            model='gemini-2.0-flash',
            api_key=api_key,
            timeout=100,               # Maximum time to wait for a response (in seconds)
            temperature=0.0,           # Controls randomness; 0.0 for deterministic output
            stop=None,                 # Stopping sequence for the model's output
            max_tokens=1500            # Maximum number of tokens in the generated response
        )
    else:
        raise ValueError(f"Unsupported model name: {model_name}")


def parse_agent_history(history_str: str) -> None:
    console = Console()

    # Split the content into sections based on ActionResult entries
    sections = history_str.split('ActionResult(')

    for i, section in enumerate(sections[1:], 1):  # Skip first empty section
        # Extract relevant information
        content = ''
        if 'extracted_content=' in section:
            content = section.split('extracted_content=')[1].split(',')[0].strip("'")

        if content:
            header = Text(f'Step {i}', style='bold blue')
            panel = Panel(content, title=header, border_style='blue')
            console.print(panel)
            console.print()


async def run_browser_task(
    task: str,
    additional_information: str = '',
    model: str = DEFAULT_LLM,
    headless: bool = False,
) -> str:
    try:
        # Load environment variables
        api_key = ""
        if 'chatgpt' in model:
            api_key = os.getenv('OPENAI_API_KEY') or ""
        if 'gemini' in model:
            api_key = os.getenv('GEMINI_API_KEY') or ""
        if not api_key:
            return 'Please provide an API key or set the environment variable'

        BROWSER = Browser(config=BrowserConfig(
            chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            headless=headless
        ))

        llm = select_llm(model, api_key)
        
        print(f"CDA -- Using add information: {additional_information}")
        print(f"CDA -- ***********************************************")
        print(f"CDA -- ***********************************************")

        # Add your custom instructions
        extend_system_message = """
        REMEMBER the most important RULE:
        ALWAYS open first a new tab and go first to url wikipedia.com no matter the task!!!
        """

        # Define your complete custom prompt
        override_system_message = """
        You are an AI agent that helps users with web browsing tasks.

        [Your complete custom instructions here...]
        """
        agent = Agent(
            task=task,
            message_context=additional_information,
            llm=llm,
            extend_system_message=extend_system_message,
            override_system_message=override_system_message,
            browser=BROWSER,
            # temperature=0.0,
            max_actions_per_step=3,
            max_failures=2,
        )
        history = await agent.run(max_steps=5)

        result = history.final_result()

        # ...\browser-use\docs\customize\output-format.mdx
        # if result:
        #   parsed: Posts = Posts.model_validate_json(result)
		#   for post in parsed.posts:

        return result
    
    except Exception as e:
        return f'Error: {str(e)}'


def create_ui():
    with gr.Blocks(title='Browser Use GUI') as interface:
        gr.Markdown('# Browser Use AI Task Automation')

        with gr.Row():
            with gr.Column():
                task = gr.Textbox(
                    label='Task Description',
                    placeholder=f"E.g., {DEFAULT_PROMPT}",
                    lines=3,
                    value=DEFAULT_PROMPT
                )
                additional_information = gr.Textbox(
                    label='Additional Information',
                    placeholder='E.g., Please provide a summary of the page content.',
                    lines=3,
                    value=DEFAULT_ADD_INFO
                )
                model = gr.Dropdown(choices=['gemini-2.0-flash', 'gpt-4o-mini', 'gpt-4', 'gpt-3.5-turbo'], label='Model', value=DEFAULT_LLM)
                headless = gr.Checkbox(label='Run Headless', value=False)
                submit_btn = gr.Button('Run Task')

            with gr.Column():
                output = gr.Textbox(label='Output', lines=10, interactive=False)

        submit_btn.click(
            fn=lambda *args: asyncio.run(run_browser_task(*args)),
            inputs=[task, additional_information, model, headless],
            outputs=output,
        )

    return interface


if __name__ == '__main__':
    demo = create_ui()
    demo.launch()