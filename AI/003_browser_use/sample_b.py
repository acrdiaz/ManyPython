import os
import sys
from typing import Optional

from pydantic import BaseModel

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext


class HoverAction(BaseModel):
    index: Optional[int] = None
    xpath: Optional[str] = None
    selector: Optional[str] = None


browser = Browser(
    config=BrowserConfig(
        headless=False,
    )
)
controller = Controller()


@controller.registry.action(
    'Hover over an element',
    param_model=HoverAction,  # Define this model with at least "index: int" field
)
async def hover_element(params: HoverAction, browser: BrowserContext):
    """
    Hovers over the element specified by its index from the cached selector map or by XPath.
    """
    session = await browser.get_session()
    state = session.cached_state

    if params.xpath:
        # Use XPath to locate the element
        element_handle = await browser.get_locate_element_by_xpath(params.xpath)
        if element_handle is None:
            raise Exception(f'Failed to locate element with XPath {params.xpath}')
    elif params.selector:
        # Use CSS selector to locate the element
        element_handle = await browser.get_locate_element_by_css_selector(params.selector)
        if element_handle is None:
            raise Exception(f'Failed to locate element with CSS Selector {params.selector}')
    elif params.index is not None:
        # Use index to locate the element
        if state is None or params.index not in state.selector_map:
            raise Exception(f'Element index {params.index} does not exist - retry or use alternative actions')
        element_node = state.selector_map[params.index]
        element_handle = await browser.get_locate_element(element_node)
        if element_handle is None:
            raise Exception(f'Failed to locate element with index {params.index}')
    else:
        raise Exception('Either index or xpath must be provided')

    try:
        await element_handle.hover()
        msg = (
            f'🖱️ Hovered over element at index {params.index}'
            if params.index is not None
            else f'🖱️ Hovered over element with XPath {params.xpath}'
        )
        return ActionResult(extracted_content=msg, include_in_memory=True)
    except Exception as e:
        err_msg = f'❌ Failed to hover over element: {str(e)}'
        raise Exception(err_msg)


async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    task = 'Open https://testpages.eviltester.com/styled/csspseudo/css-hover.html and hover the element with the css selector #hoverdivpara, then click on "Can you click me?"'
    # task = 'Open https://testpages.eviltester.com/styled/csspseudo/css-hover.html and hover the element with the xpath //*[@id="hoverdivpara"], then click on "Can you click me?"'
    model = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash',
        google_api_key=api_key,
        temperature=0.2,
    )
    agent = Agent(
        task=task,
        llm=model,
        controller=controller,
        browser=browser,
    )

    await agent.run()
    await browser.close()

    input('Press Enter to close...')


if __name__ == '__main__':
    asyncio.run(main())

# from langchain_google_genai import ChatGoogleGenerativeAI
# from browser_use.browser.context import BrowserContextConfig
# from browser_use import Agent, Browser, Controller
# from browser_use.browser.context import BrowserContext
# import asyncio
# from pydantic import SecretStr
# import os
# from dotenv import load_dotenv
# from getpass import getpass

# # Load environment variables
# load_dotenv()

# async def main():
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         raise ValueError("GEMINI_API_KEY not found in environment variables.")

#     # Get credentials
#     username = "admin" # input("Username (default: admin): ").strip() or "admin"
#     password = "password" # getpass("Password (default: admin): ").strip() or "password"
    
#     # Get project name
#     project_name = input("Project name to open: ").strip()
#     if not project_name:
#         raise ValueError("Project name cannot be empty")

#     # Separate controller functions
#     async def credentials_controller():
#         return {"username": username, "password": password}

#     async def project_controller():
#         return {"project_name": project_name}

#     prompt = f"""
#     1. Login to ... using provided credentials: credentials_controller()
#     2. Verify successful login
#     3. Search for project using provided name
#     4. Open the project
#     5. Verify project dashboard appears
#     6. Return confirmation message
#     """

#     # Initialize the Gemini model
#     llm = ChatGoogleGenerativeAI(
#         model='gemini-1.5-flash',
#         google_api_key=SecretStr(api_key),
#         temperature=0.2,
#     )

#     config = BrowserContextConfig(
#         wait_for_network_idle_page_load_time=3.0,
#         browser_window_size={'width': 800, 'height': 600},
#         locale='en-US',
#         highlight_elements=True,
#     )

#     browser = Browser()
#     context = BrowserContext(browser=browser, config=config)
#     controller = Controller()
#     registry = controller.registry

#     # Register controllers as actions
#     @registry.action(description='Use credentials')
#     async def credentials_action():
#         return await credentials_controller()

#     @registry.action(description='Provide project name')
#     async def project_action():
#         return await project_controller()

#     try:
#         # Create the Agent with the controller
#         agent = Agent(
#             task=prompt,
#             llm=llm,
#             browser_context=context,
#             controller=controller,
#             max_actions_per_step=2
#         )

#         # Run the agent
#         print(f"\nOpening project '{project_name}'...")
#         result = await agent.run()
#         print(f"\n✅ {result}")
#     finally:
#         await context.close()
#         await browser.close()

# if __name__ == '__main__':
#     asyncio.run(main())