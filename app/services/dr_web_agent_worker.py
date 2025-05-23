import asyncio
import logging
import os
import threading

from browser_use import Agent, Browser, BrowserConfig
from concurrent.futures import Executor, ThreadPoolExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from functools import partial


MAX_STEPS = 30
MAX_ACTIONS_PER_STEP = 10

API_KEY = SecretStr(os.getenv("GEMINI_API_KEY")) # type: ignore
LLM_GEMINI = 'gemini-2.0-flash'
LLM_GPT = 'gpt-4o-mini'

DEFAULT_MODEL = LLM_GEMINI


class DRWebAgentWorker:
    def __init__(self, browser_name = "chrome", executor: Executor = None):  # type: ignore
        self._loop = asyncio.new_event_loop()
        self.executor = executor or ThreadPoolExecutor(max_workers=4)
        self._running = False

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
    # def process(self, prompt, callback=None):
    #     # """Submit prompt for processing"""
    #     # future = self.executor.submit(self._execute_agent_work, prompt, self.browser)
    #     # if callback:
    #     #     future.add_done_callback(callback)
    #     # return future
    #     """Bridge sync world to async"""
    #     async def _run_and_notify():
    #         result = await self._execute_agent_work(prompt)
    #         if callback:
    #             callback(result)
    #         return result

    #     future = asyncio.run_coroutine_threadsafe(
    #         _run_and_notify(),
    #         self._loop
    #     )
    #     return future

    # @staticmethod
    # async def _execute_agent_work(prompt="", browser=None):
    #     if browser is None: 
    #         raise ValueError("Browser instance is required")
    #     if not prompt:
    #         raise ValueError("Prompt is required")
        
    #     logging.info(f"Agent started processing: {prompt}")

    #     llm = ChatGoogleGenerativeAI(
    #         model=DEFAULT_MODEL,
    #         api_key=API_KEY,
    #     )

    #     agent = Agent(
    #         task=prompt,
    #         llm=llm,
    #         browser=browser,
    #     )
        
    #     await agent.run()
    #     await agent.browser.close()

    #     return f"Processed: {prompt}"

    # def start(self):
    #     """Start event loop in background thread"""
    #     self._running = True
    #     threading.Thread(
    #         target=self._run_event_loop,
    #         daemon=True
    #     ).start()

    # def _run_event_loop(self):
    #     """Run the event loop in dedicated thread"""
    #     asyncio.set_event_loop(self._loop)
    #     while self._running:
    #         self._loop.run_forever()

    def shutdown(self):
        """Cleanup resources"""
        self._running = False
        self._loop.call_soon_threadsafe(self._loop.stop)
        self.executor.shutdown(wait=True)

if __name__ == "__main__":
    prompt = "open https://espanol.yahoo.com/"
    buService = DRWebAgentWorker("chrome")
    asyncio.run(buService.main(prompt))