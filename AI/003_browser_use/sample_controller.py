"""
Show how to use custom outputs.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

# import json
import os
import sys
# from typing import List

# import requests

from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI
#from pydantic import BaseModel

from browser_use import Agent, Controller



# class Profile(BaseModel):
#     platform: str
#     profile_url: str


# class Profiles(BaseModel):
#     profiles: List[Profile]


controller = Controller(
    # exclude_actions=['search_google'],
    # output_model=Profiles
)


@controller.registry.action('Get message from page')
async def get_message(query: str):
    # keys_to_use = ['url', 'title', 'content', 'author', 'score']
    # headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    # response = requests.post('https://asktessa.ai/api/search', headers=headers, json={'query': query})

    # final_results = [
    # {key: source[key] for key in keys_to_use if key in source}
    #     for source in response.json()['sources']
    #     if source['score'] >= 0.2
    # ]
    # # print(json.dumps(final_results, indent=4))
    # result_text = json.dumps(final_results, indent=4)
    # print(result_text)
    result_text = "Summary: CDA cool!!!"
    print(f"CDA - Search result: {result_text}")
    print("*********")
    #return ActionResult(extracted_content=result_text, include_in_memory=True)
    return result_text


async def main():
    task = """
    get the Result with get_message
    """
    
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        api_key=os.getenv('GEMINI_API_KEY')
    )

    model = llm
    agent = Agent(
        task=task,
        llm=model,
        controller=controller
    )

    history = await agent.run()

    print(history)

    # if history:
    #     parsed: Profiles = Profiles.model_validate_json(history)

    #     for profile in parsed.profiles:
    #         print('\n--------------------------------')
    #         print(f'Platform:       {profile.platform}')
    #         print(f'Profile URL:    {profile.profile_url}')

    # else:
    #     print('No result')

if __name__ == '__main__':
    asyncio.run(main())