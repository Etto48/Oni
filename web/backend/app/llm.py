import openai
import inspect

from pydantic import BaseModel

from models import ChatMessage
from tools import InternetQueryArgs, debug_tool, function_list, internet_query

class LLM:
    def __init__(self, url: str,  model: str, api_key: str = ""):
        self.url = url
        self.model = model
        self.api_key = api_key
        self.client = openai.AsyncOpenAI(base_url=self.url, api_key=self.api_key)

    @staticmethod
    def _function_tool_schema(func: callable, args: BaseModel | None) -> dict:
        schema = {
            "type": "function",
            "name": func.__name__,
            "description": inspect.getdoc(func) or "",
            "parameters": args.model_json_schema() if args else {},
        }
        return schema

    async def chat_completion(self, messages: list[ChatMessage]):
        tools = [
            self._function_tool_schema(
                func=function_list,
                args=None
            ),
            self._function_tool_schema(
                func=internet_query,
                args=InternetQueryArgs
            ),
            self._function_tool_schema(
                func=debug_tool,
                args=None
            ),
        ]
        print("Sending request to LLM with tools:", tools)
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": message.role,
                "content": message.content
            } for message in messages],
            tools=tools,
            stream=True
        )
        async for chunk in response:
            print(chunk)
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content