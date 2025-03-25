# pip install -U langchain-google-genai

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from pydantic import SecretStr
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def main():
    try:
        # Retrieve API key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            return

        # Define the prompt
        prompt = """
            go to https://qa-tmplus.wktmdev.com/TeamMate, with credentials user: admin, pass: password
            Open the "project section" using the main menu
            the project section will display the list of projects,
            Open the first project using the ribbon.
            Once the project is opened
            get the project url
            log out from the application
        """

        # Initialize the model
        llm = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash-exp', 
            api_key=SecretStr(api_key)
        )

        # Create agent with the model
        agent = Agent(
            task=prompt,
            llm=llm
        )

        # Run the agent
        logger.info("Running agent...")
        await agent.run()
        logger.info("Agent execution completed.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

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

#print(os.environ["BROWSER"])
