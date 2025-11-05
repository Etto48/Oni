import httpx
from pydantic import BaseModel, Field

class InternetQueryArgs(BaseModel):
    url: str = Field(..., description="The URL of the web page to fetch.")

async def internet_query(args: InternetQueryArgs) -> str:
    """Fetch the content of a web page given its URL."""
    response = await httpx.AsyncClient().get(args.url)
    return response.text

async def debug_tool() -> str:
    """A simple debug tool that returns 'Ok'."""
    return "Ok"

async def function_list():
    """Return a list of available function tools."""
    return ["function_list", "internet_query", "debug_tool"]