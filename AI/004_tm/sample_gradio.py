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
DEFAULT_PROMPT = 'What is todays date in Spanish'


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
        
        agent = Agent(
            task=task,
            llm=llm,
            browser=BROWSER,
        )
        history = await agent.run()
        result = history.final_result()
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
                model = gr.Dropdown(choices=['gemini-2.0-flash', 'gpt-4o-mini', 'gpt-4', 'gpt-3.5-turbo'], label='Model', value=DEFAULT_LLM)
                headless = gr.Checkbox(label='Run Headless', value=False)
                submit_btn = gr.Button('Run Task')

            with gr.Column():
                output = gr.Textbox(label='Output', lines=10, interactive=False)

        submit_btn.click(
            fn=lambda *args: asyncio.run(run_browser_task(*args)),
            inputs=[task, model, headless],
            outputs=output,
        )

    return interface


if __name__ == '__main__':
    demo = create_ui()
    demo.launch()