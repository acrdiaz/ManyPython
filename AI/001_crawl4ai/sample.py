# Install Crawl4AI:

# Install the package
#   pip install -U crawl4ai

# For pre release versions
#   pip install crawl4ai --pre

# Run post-installation setup
#   crawl4ai-setup

# Verify your installation
#  crawl4ai-doctor

# If you encounter any browser-related issues, you can install them manually:
#   python -m playwright install --with-deps chromium

# Notes:
# https://github.com/unclecode/crawl4ai
# https://pypi.org/project/crawl4ai/
# https://github.com/coleam00/ottomator-agents/blob/main/crawl4AI-agent/crawl4AI-examples/1-crawl_single_page.py
# https://github.com/pydantic/pydantic-ai

import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://ai.pydantic.dev",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())