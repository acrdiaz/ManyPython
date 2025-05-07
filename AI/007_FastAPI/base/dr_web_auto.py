import os
import asyncio

from browser_use.agent.views import ActionResult # AgentHistoryList
from browser_use import Agent # Controller # AA1
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


class DRWebAuto:
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

    DEFAULT_MODEL = LLM_GEMINI

    def __init__(self):
        print("OK dRWebAuto")
    
    def get_model_instance(self, model_choice):
        """Returns the appropriate model instance based on user choice."""
        if model_choice == self.LLM_GEMINI:
            return ChatGoogleGenerativeAI(
                model=self.LLM_GEMINI,
                api_key=self.API_KEY,
                temperature=0.0,
                # max_tokens=32000
            )
        elif model_choice == self.LLM_GPT:
            return ChatOpenAI(
                model=self.LLM_GPT,
                temperature=0.0,
            )
        return None

    async def run_agent(
            self,
            llm,
            prompt,
            additional_information=None,
            # planner_llm,
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
            browser=self.BROWSER,
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
            max_actions_per_step=self.MAX_ACTIONS_PER_STEP,
            # validate_output=True,
            # max_input_tokens=64000,
            max_failures=2,                             # Increase max failures to allow for retries
            retry_delay=3,                            # Short delay between retries
            # # enable_memory=True                      # Enable memory to remember failed attempts
            # tool_calling_method='function_calling'      # Add this line
        )

        page_content = await agent.run(max_steps=self.MAX_STEPS)  # Increase max steps to allow for recovery, 3 steps
        # page_content = await agent.run()
        return page_content
