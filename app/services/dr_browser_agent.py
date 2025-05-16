import asyncio
import logging
import os
import time
from typing import Optional, Dict, Any, List, Union

from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

# Configure logging
logger = logging.getLogger('BrowserAgent')

class DRBrowserUseAgent:
    """
    A wrapper class for the browser-use package that provides a simplified interface
    for running browser automation tasks.
    """
    
    def __init__(self, 
                 browser_name: str = "edge", 
                 api_key: Optional[str] = None,
                 headless: bool = False,
                 timeout: int = 60,
                 model: str = 'gemini-2.0-flash'):
        """
        Initialize the browser agent.
        
        Args:
            browser_name: The name of the browser to use (edge, chrome, firefox)
            api_key: The API key for the LLM. If None, will try to get from environment.
            headless: Whether to run the browser in headless mode
            timeout: Timeout in seconds for browser operations
            model: The model to use for the LLM
        """
        self.browser_name = browser_name.lower()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.headless = headless
        self.timeout = timeout
        self.model = model
        self.browser_paths = {
            "edge": [
                'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
                'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe'
            ],
            "chrome": [
                'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
            ],
            "firefox": [
                'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe',
                'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
            ]
        }
        
        logger.info(f"Initialized DRBrowserUseAgent with browser: {browser_name}, headless: {headless}")
    
    def _get_browser_path(self) -> str:
        """
        Get the path to the browser executable.
        
        Returns:
            The path to the browser executable
        
        Raises:
            FileNotFoundError: If the browser executable is not found
        """
        if self.browser_name not in self.browser_paths:
            logger.warning(f"Unknown browser: {self.browser_name}, defaulting to edge")
            self.browser_name = "edge"
        
        # Check if any of the paths exist
        for path in self.browser_paths[self.browser_name]:
            if os.path.exists(path):
                return path
        
        # If no path exists, raise an error
        raise FileNotFoundError(f"Browser executable not found for {self.browser_name}")
    
    def _create_browser(self) -> Browser:
        """
        Create a browser instance.
        
        Returns:
            A browser instance
        """
        browser_path = self._get_browser_path()
        logger.info(f"Creating browser with path: {browser_path}")
        
        return Browser(
            config=BrowserConfig(
                chrome_instance_path=browser_path,
                headless=self.headless,
                timeout=self.timeout
            )
        )
    
    def _create_llm(self):
        """
        Create an LLM instance.
        
        Returns:
            An LLM instance or None if no API key is provided
        """
        if not self.api_key:
            logger.warning("No API key provided for LLM")
            return None
        
        return ChatGoogleGenerativeAI(
            model=self.model,
            api_key=SecretStr(self.api_key)
        )
    
    async def main(self, task: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run the browser agent with the given task.
        
        Args:
            task: The task to perform
            metadata: Additional metadata for the task
            
        Returns:
            A dictionary with the result of the task
        """
        start_time = time.time()
        logger.info(f"Running browser agent with task: {task[:50]}...")
        
        result = {
            "status": "error",
            "message": "",
            "task": task,
            "metadata": metadata or {},
            "duration": 0,
            "timestamp": start_time
        }
        
        try:
            browser = self._create_browser()
            llm = self._create_llm()
            
            if not llm:
                result["message"] = "Error: No API key provided for LLM"
                return result
            
            agent = Agent(
                task=task,
                llm=llm,
                browser=browser,
            )
            
            # Run the agent
            await agent.run()
            
            # Get the result
            result["status"] = "success"
            result["message"] = "Task completed successfully"
            
            # Add agent results if available
            if hasattr(agent, 'result'):
                result["agent_result"] = agent.result
            
            return result
        except Exception as e:
            logger.error(f"Error running browser agent: {str(e)}")
            result["message"] = f"Error: {str(e)}"
            return result
        finally:
            # Close the browser
            if 'browser' in locals():
                await browser.close()
            
            # Calculate duration
            result["duration"] = time.time() - start_time
    
    @classmethod
    async def run_task(cls, task: str, browser_name: str = "edge", **kwargs) -> Dict[str, Any]:
        """
        Run a task with the browser agent.
        
        Args:
            task: The task to perform
            browser_name: The name of the browser to use
            **kwargs: Additional arguments for the browser agent
            
        Returns:
            A dictionary with the result of the task
        """
        agent = cls(browser_name=browser_name, **kwargs)
        return await agent.main(task)

# Example usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    async def run_example():
        agent = DRBrowserUseAgent(browser_name="chrome")
        result = await agent.main("Search for 'Python programming'")
        print(f"Result: {result}")
    
    asyncio.run(run_example())