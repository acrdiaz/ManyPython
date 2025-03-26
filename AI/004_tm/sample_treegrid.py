from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from pydantic import SecretStr
import os
from dotenv import load_dotenv

async def navigate_treegrid():
    """
    Streamlined workflow for navigating complex tree grid
    """
    # Load API key from environment
    api_key = os.getenv("GEMINI_API_KEY")

    # Concise, targeted prompt
    prompt = f"""
    Workflow for TreeGrid Navigation:
    1. Login to https://qa-tmplus.wktmdev.com/TeamMate
       - Username: admin
       - Password: password

    2. Navigate to Project Section:
       - Open main menu
       - Select 'Project' section
       - Open first available project

    3. TreeGrid Exploration Strategy:
       - Confirm tree grid is loaded
       - Identify total number of rows
       - Focus on:
         * Rows that can be expanded
         * Handling multi-level hierarchies
         * Collecting key information from expanded rows

    Key Exploration Guidelines:
    - Expand rows systematically
    - Handle partially expanded rows
    - Avoid redundant expansions
    - Capture meaningful row details
    """

    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash-exp', 
        api_key=SecretStr(api_key)
    )

    # Create agent with the simplified approach
    agent = Agent(
        task=prompt,
        llm=llm,
        credentials={
            'username': 'admin',
            'password': 'password'
        }
    )

    # Execute the workflow
    await agent.run()

async def main():
    try:
        # Load environment variables
        load_dotenv()

        # Run the treegrid navigation
        await navigate_treegrid()

    except Exception as e:
        print(f"Navigation Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())