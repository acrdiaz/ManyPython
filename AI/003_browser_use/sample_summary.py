# pip install -U langchain-google-genai browser-use python-dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent  # Assuming this is your custom or third-party module
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration constants
TARGET_URL = 'https://en.wikipedia.org/wiki/Audit_working_papers' #'https://en.wikipedia.org/wiki/Summary'
SUMMARY_LENGTH = 2  # sentences
MODEL_NAME = 'gemini-2.0-flash'

async def main():
    # Retrieve the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")

    # Define the task for the agent
    prompt = f"""
        Go to {TARGET_URL}, extract the main content of the page, and return it as plain text.
    """

    try:
        # Initialize the AI model
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            api_key=api_key
        )

        # Create an agent to extract the page content
        agent = Agent(
            task=prompt,
            llm=llm
        )
        print(f"Fetching content from {TARGET_URL}...")
        page_content = await agent.run()

        # Ensure the agent returned valid content
        if not page_content: #or not isinstance(page_content, str):
            raise ValueError("Agent returned invalid or empty content.")

        # Generate a summary of the page content
        summary_prompt = f"""
            Summarize the following content in exactly {SUMMARY_LENGTH} concise sentences.
            Focus on key facts and main ideas.
            Return only the summary without additional commentary.
            
            Content:
            {page_content.history[-1].result[-1].extracted_content[:10000]}  # Limit input size to avoid exceeding token limits
        """
        print("Generating summary...")
        summary_result = llm.invoke(summary_prompt)  # Use invoke() instead of generate_content()
        summary = summary_result.content.strip()

        # Print the summary
        print("\nAI Summary:\n", summary)

    except Exception as e:
        print("Process failed:", e)
        exit(1)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())