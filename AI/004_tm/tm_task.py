from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from pydantic import SecretStr
import os
from dotenv import load_dotenv
#load_dotenv()

async def main():
  api_key = os.getenv("GEMINI_API_KEY")

  prompt = f"""
      go to https://www.calendardate.com/todays.htm, and tell me what day it is today and the timezone.
      """

  # Initialize the model
  llm = ChatGoogleGenerativeAI(
      model='gemini-2.0-flash-exp', 
      api_key=SecretStr(os.getenv('GEMINI_API_KEY'))
  )

  # Create agent with the model
  agent = Agent(
      task = prompt,
      llm = llm
  )

  await agent.run()

asyncio.run(main())

