import asyncio
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

# Third-party imports
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Local module imports
from browser_use import Agent, Browser, BrowserConfig



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


# Append the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BROWSER = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
)

SUMMARY_LENGTH = 2  # sentences


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


def select_llm(model_name, api_key):
    if 'chatgpt' in model_name.lower():
        return ChatOpenAI(
            model='gpt-4o-mini',
            timeout=100,               # Maximum time to wait for a response (in seconds)
            temperature=0.0,           # Controls randomness; 0.0 for deterministic output
            stop=None,                 # Stopping sequence for the model's output
            max_tokens=1500)           # Maximum number of tokens in the generated response
    elif 'gemini' in model_name.lower():
        return ChatGoogleGenerativeAI(
            model='gemini-2.0-flash', 
            api_key=api_key,
            timeout=100,               # Maximum time to wait for a response (in seconds)
            temperature=0.0,           # Controls randomness; 0.0 for deterministic output
            stop=None,                 # Stopping sequence for the model's output
            max_tokens=1500)           # Maximum number of tokens in the generated response
    else:
        raise ValueError(f"Unsupported model name: {model_name}")


def load_file(file_path):
    cwd = os.getcwd()
    if '004_tm' not in cwd:
        os.chdir(Path(cwd).joinpath('AI/004_tm'))

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")


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


async def run_browser_task(
    task: str,
    api_key: str,
    model: str = 'gpt-4o',
    headless: bool = True,
) -> str:
    if not api_key.strip():
        if 'chatgpt' in model:
            api_key = os.getenv('OPENAI_API_KEY') or ""
        if 'gemini' in model:
            api_key = os.getenv('GEMINI_API_KEY') or ""
        if not api_key:
            return 'Please provide an API key or set the environment variable'

    llm = select_llm(model, api_key)

    try:
        agent = Agent(
            task=task,
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
        history = await agent.run()
        result = history.final_result()
        # ...get_summary AA1 maybe not here
        #  The result cloud be parsed better
        return result or ""
    except Exception as e:
        return f'Error: {str(e)}'


def create_ui():
    with gr.Blocks(title='Browser Use GUI') as interface:
        gr.Markdown('# Browser Use Task Automation')

        with gr.Row():
            with gr.Column():
                api_key = gr.Textbox(
                    label='LLM API Key', 
                    info='Your API key (leave blank to use .env)',
                    placeholder='sk-...', 
                    type='password'
                )
                task = gr.Textbox(
                    label='Task Description',
                    info='Describe what you want the agent to do',
                    placeholder='E.g., Find todays date in json format',
                    lines=3,
                    value='sample ABC'
                )
                additional_info = gr.Textbox(
                    label='Additional Information',
                    info='Optional hints to help the LLM complete the task',
                    placeholder='Enter any additional details here...',
                    lines=3
                )
                model = gr.Dropdown(choices=['gemini-2.0-flash', 'gpt-4o-mini', 'gpt-4', 'gpt-3.5-turbo'], label='Model', value='gpt-4o-mini')
                options = gr.Dropdown(choices=['', 'Get-Summary', 'bb', 'cc'], label='Options', value='')
                headless = gr.Checkbox(label='Run Headless', value=False)
                submit_btn = gr.Button('Run Task')

            with gr.Column():
                output = gr.Textbox(label='Output', lines=10, interactive=False)
        
        # Add event handler for options dropdown
        def update_task(option_value):
            if not option_value:
                return ""
            if option_value == 'Get-Summary':
                prompt = load_file('02_prompt_extract_text.txt')
                return prompt
            return f'Selected: {option_value}'
            
        options.change(
            fn=update_task,
            inputs=[options],
            outputs=[task]
        )

        submit_btn.click(
            fn=lambda *args: asyncio.run(run_browser_task(*args)),
            inputs=[task, api_key, model, headless],
            outputs=output,
        )

    return interface


if __name__ == '__main__':
    demo = create_ui()
    demo.launch()
