from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from pydantic import SecretStr
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables securely
load_dotenv()

async def get_today_info() -> Optional[str]:
    """Fetch today's date and timezone using browser automation with error handling."""
    try:
        prompt = """
        Go to https://www.calendardate.com/todays.htm and extract:
        1. Today's full date (e.g., 'Monday, June 10, 2024')
        2. The timezone mentioned on the page
        Return ONLY these two pieces of information in JSON format like:
        {"date": "...", "timezone": "..."}
        """
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            api_key=SecretStr(os.getenv("GEMINI_API_KEY")),
            temperature=0.3  # More deterministic output
        )

        agent = Agent(task=prompt, llm=llm)
        result = await agent.run()
        
        # Validate minimal response
        if not result or len(result.history) < 2: # Basic sanity check
            raise ValueError("Insufficient response from agent")
        
        # if result.history[-1].result[-1].extracted_content \
        #    and result.history[-1].result[-1].is_done == True \
        #    and result.history[-1].result[-1].success == True:
        #     return result.history[-1].result[-1].extracted_content
        return result.history[-1].result[-1].extracted_content
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

async def main():
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Missing GEMINI_API_KEY in environment variables")
    
    response = await get_today_info()
    
    if response:
        print("Successfully retrieved data:")
        print(response)
    else:
        print("Failed to retrieve data")

if __name__ == "__main__":
    asyncio.run(main())