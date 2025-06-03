# pip install -U langchain-google-genai

from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

import asyncio
import os


MAX_STEPS = 30
MAX_ACTIONS_PER_STEP = 10

API_KEY = SecretStr(os.getenv("GEMINI_API_KEY"))
LLM_GEMINI = 'gemini-2.0-flash'
LLM_GPT = 'gpt-4o-mini'

DEFAULT_MODEL = LLM_GEMINI


class DRBrowserUseAgent:
    def __init__(self, browser_name: str) -> None:
        """Initialize the browser use service.

        Args:
            browser_name (str): Name of the browser to be used
        """
        if browser_name == "chrome":
            path_32 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            path_64 = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        elif browser_name == "edge":
            path_32 = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            path_64 = "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
        else:
            raise FileNotFoundError(f"Browser not supported: {browser_name}")

        path = self.app_exits(path_32, path_64)

        if path is None:
            raise FileNotFoundError(f"Browser path file not found: {browser_name}")

        self.browser = Browser(
            config=BrowserConfig(
                chrome_instance_path=path,
            )
        )
    
    def app_exits(self, path_32, path_64):
        """Check if the application exists in the given paths.

        Args:
            folder_path_32 (str): Path to the 32-bit application
            folder_path_64 (str): Path to the 64-bit application

        Returns:
            str: Path of the existing application or None
        """
        if os.path.exists(path_32):
            return path_32
        elif os.path.exists(path_64):
            return path_64
        else:
            return None

    async def main(self, prompt = ""):  
        llm = ChatGoogleGenerativeAI(
            model=DEFAULT_MODEL,
            api_key=API_KEY,
        )

        agent = Agent(
            task=prompt,
            llm=llm,
            browser=self.browser,
        )
        
        await agent.run()
        await agent.browser.close()


if __name__ == "__main__":
    prompt = "open https://espanol.yahoo.com/"
    buService = DRBrowserUseAgent("edge")
    asyncio.run(buService.main(prompt))