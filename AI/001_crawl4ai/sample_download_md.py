import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://ai.pydantic.dev",
        )
        
        markdown_content = result.markdown
        print("markdown_content")
        
        # Save the markdown content to a file
        with open("output.md", "w") as file:
            file.write(markdown_content)

if __name__ == "__main__":
    asyncio.run(main())