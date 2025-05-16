# pip install langchain-google-genai
# pip install browser-use
# pip install requests

from browser_use import Agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional
from pydantic import SecretStr
import asyncio
import os
import logging
import requests

# Load environment variables securely
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_notification(message: str):
    """
    Send a notification with the given message.
    """
    try:
        # Example: Send a POST request to a webhook or notification service
        webhook_url = os.getenv("WEBHOOK_URL")
        if webhook_url:
            response = requests.post(webhook_url, json={"text": message})
            response.raise_for_status()
            logging.info("Notification sent successfully.")
        else:
            logging.warning("WEBHOOK_URL not set. Notification not sent.")
    except Exception as e:
        logging.error(f"Failed to send notification: {str(e)}")

async def navigate_treegrid() -> Optional[str]:
    """
    Streamlined workflow for navigating complex tree grid and returning results in JSON format.
    """
    try:
        # Load API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY in environment variables")

        # Concise, targeted prompt
        prompt = """
        Workflow for TreeGrid Navigation:

        1. Login to ...
        - Use credentials: admin.-- password

        2. Navigate to Project Section:
        - Open the main menu
        - Select the 'Project' section
        - The list displays all projects
        - Click on the project name: 05: German - Translations.com - Project
        - Open it using double-click or the ribbon button 'Open'

        3. TreeGrid Exploration:
        - review expand/collapse status for node 'Corporate Accounting'
        - if node is collapsed then expand the node 'Corporate Accounting'
        - the node 'Corporate Accounting' has children, List the names of the 1st level children (objects) in JSON format like:
        {"children": ["Child1", "Child2", ...]}
        - Log any issues encountered during tree grid exploration

        Key Exploration Guidelines:
        - treegrid Focus on the rows, not the columns
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
        logging.error(f"Error: {str(e)}")
        send_notification(f"Error encountered: {str(e)}")
        return None

async def main():
    response = await navigate_treegrid()
    
    if response:
        logging.info("Successfully retrieved data:")
        logging.info(response)
    else:
        logging.error("Failed to retrieve data")

if __name__ == "__main__":
    asyncio.run(main())