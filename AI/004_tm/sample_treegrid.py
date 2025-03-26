# pip install langchain-google-genai
# pip install browser-use

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from pydantic import SecretStr
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables securely
load_dotenv()

async def navigate_treegrid() -> Optional[str]:
    """
    Streamlined workflow for navigating complex tree grid and returning results in JSON format.
    """
    try:
        # Load API key from environment
        api_key = os.getenv("GEMINI_API_KEY")

        # Concise, targeted prompt
        # project:
        # 05: German - Translations.com - Project
        prompt = """
        Workflow for TreeGrid Navigation:

        1. Login to https://rc-sample.wktmdev.com/TeamMate
        - Username: admin.cd
        - Password: password

        2. Navigate to Project Section:
        - Open the main menu
        - Select the 'Project' section
        - Open the project: 05: German - Translations.com - Project
        - To open a project, use double-click or use the ribbon button 'Open'
        - Ensure the project is opened and fully loaded

        3. TreeGrid Exploration Strategy:
        - Confirm the tree grid is loaded
        - Identify the total number of rows
        - Focus on:
            * Rows that can be expanded
            * Handling multi-level hierarchies
            * Collecting key information from expanded rows

        4. Specific Task:
        - Check if the node 'Corporate Accounting' is expanded
        - If collapsed, expand the node 'Corporate Accounting'
        - List the names of the 1st level children (objects) in JSON format like:
        {"children": ["Child1", "Child2", ...]}

        Key Exploration Guidelines:
        - Expand rows systematically
        - Handle partially expanded rows
        - Avoid redundant expansions
        - Capture meaningful row details

        Special Considerations:
        - The expand/collapse control is located to the left
        - Use the '>>' button to display the 'Form View' panel
        - Use the kebab menu (three vertical dots) for more options: expand, add objects to the tree
        - Some tree elements may be collapsed, while others may be expanded
        """

        # Initialize the Gemini model
        llm = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash', 
            api_key=SecretStr(api_key)
        )

        # Create agent with the simplified approach
        agent = Agent(
            task=prompt,
            llm=llm
        )

        # Execute the workflow
        result = await agent.run()

        # Validate minimal response
        if not result or len(result.history) < 2: # Basic sanity check
            raise ValueError("Insufficient response from agent")

        return result.history[-1].result[-1].extracted_content

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

async def main():
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Missing GEMINI_API_KEY in environment variables")
    
    response = await navigate_treegrid()
    
    if response:
        print("Successfully retrieved data:")
        print(response)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    asyncio.run(main())