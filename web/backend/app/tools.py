import httpx
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field
import bs4

class InternetQueryArgs(BaseModel):
    url: str = Field(..., description="The URL of the web page to fetch.")

async def internet_query(args: InternetQueryArgs) -> str:
    """Fetch the content of a web page given its URL."""
    return "Internet query tool is currently disabled."
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    async with httpx.AsyncClient() as client:
        response = await client.get(args.url, headers={"User-Agent": user_agent})
        if response.status_code // 100 == 3:
            response = await client.get(response.headers['Location'], headers={"User-Agent": user_agent})
    if response.status_code != 200:
        return f"Error: Unable to fetch the URL. Status code: {response.status_code}"
    # Remove <script> and <style> tags and their content
    import re
    cleaned_text = re.sub(r'<(script|style).*?>.*?</\1>', '', response.text, flags=re.DOTALL)
    return cleaned_text

class SearchArgs(BaseModel):
    query: str = Field(..., description="The search query string.")

async def search(args: SearchArgs) -> str:
    """Perform a web search."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(args.query, max_results=5):
            results.append(f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}\n")
    return "\n".join(results)
    