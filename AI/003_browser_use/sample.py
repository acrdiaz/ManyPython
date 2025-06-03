# pip install -U langchain-google-genai

from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

import asyncio
import os


BROWSER = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    )
)


async def main():
  api_key = os.getenv("GEMINI_API_KEY")

  prompt = f"""
      go to yahoo.com
      """

  # Initialize the model
  llm = ChatGoogleGenerativeAI(
      model='gemini-2.0-flash', 
      api_key=SecretStr(os.getenv('GEMINI_API_KEY'))
  )

  # Create agent with the model
  agent = Agent(
      task = prompt,
      llm = llm,
      browser=BROWSER,
  )

  await agent.run()

if __name__ == "__main__":
    asyncio.run(main())