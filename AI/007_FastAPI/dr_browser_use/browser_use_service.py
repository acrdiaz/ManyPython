# pip install -U langchain-google-genai

from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

import asyncio
import os


BROWSER = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
)
MAX_STEPS = 30
MAX_ACTIONS_PER_STEP = 10

API_KEY = SecretStr(os.getenv("GEMINI_API_KEY"))
LLM_GEMINI = 'gemini-2.0-flash'
LLM_GPT = 'gpt-4o-mini'

DEFAULT_MODEL = LLM_GEMINI

class DRBrowserUseService:
    async def main(self, prompt = ""):  
        llm = ChatGoogleGenerativeAI(
            model=DEFAULT_MODEL,
            api_key=API_KEY,
        )

        agent = Agent(
            task=prompt,
            llm=llm,
            browser=BROWSER,
        )
        
        await agent.run()
        await agent.browser.close()


if __name__ == "__main__":
    prompt = "open https://espanol.yahoo.com/"
    buService = DRBrowserUseService()
    asyncio.run(buService.main(prompt))