import os
import asyncio
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent

# Set the BROWSER environment variable to use Edge
os.environ["BROWSER"] = "msedge"

async def main():
    api_key = os.getenv("GEMINI_API_KEY")

    prompt = f"""go to https://www.calendardate.com/todays.htm, and tell me what day it is today and the timezone.
    """

    # Initialize the model
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash', 
        api_key=SecretStr(os.getenv('GEMINI_API_KEY'))
    )

    # Create agent with the model
    agent = Agent(
        task=prompt,
        llm=llm,
        browser=os.environ["BROWSER"]  # Specify Edge browser AA1
    )

    # Run the agent with error handling
    try:
        await agent.run()
    except Exception as e:
        print(f"Error running agent: {e}")

asyncio.run(main())


    # prompt = f"""
    #   go to https://qa-tmplus.wktmdev.com/TeamMate, with credentials user: admin, pass: password
    #   Open the "project section" using the main menu
    #   the project section will display the list of projects,
    #   click select the first project
    #   using the ribbon open the selected porject
    #   now, you will see the details of a project
    #   get me the project name and url
    #   logout from the system
    # """

print(os.environ["BROWSER"])
