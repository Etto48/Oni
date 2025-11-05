from typing import AsyncGenerator
import openai
import inspect

from pydantic import BaseModel

from models import ChatMessage, StopAsyncGenerator, WSResponse
from tools import InternetQueryArgs, internet_query, SearchArgs, search
import logging

logger = logging.getLogger("llm")

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
            "function": {
                "name": func.__name__,
                "description": inspect.getdoc(func) or "",
                "parameters": args.model_json_schema() if args else {},
            }
        }
        return schema

    async def chat_completion(self, messages: list[ChatMessage]):
        tools = [
            self._function_tool_schema(
                func=internet_query,
                args=InternetQueryArgs
            ),
            self._function_tool_schema(
                func=search,
                args=SearchArgs
            ),
        ]
        chat_messages = [message.model_dump() for message in messages]
        new_messages: list[ChatMessage] = []
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=chat_messages,
            tools=tools,
            tool_choice="auto",
            stream=True
        )
        while True:
            tool_calls = []
            text = ""
            async for chunk in response:
                delta = chunk.choices[0].delta.model_dump()
                if delta["content"]:
                    text += delta["content"]
                    yield WSResponse(kind="text", text=delta["content"])
                if delta.get("tool_calls"):
                    tool_calls.extend(delta["tool_calls"])
                    yield WSResponse(kind="tool_calls", tool_calls=delta["tool_calls"])
                if delta.get("reasoning"):
                    yield WSResponse(kind="reasoning", reasoning=delta["reasoning"])
            if text != "":
                new_messages.append(ChatMessage(
                    role="assistant",
                    content=text,
                ))
            if len(tool_calls) == 0:
                break
            new_messages.append(ChatMessage(
                role="assistant",
                tool_calls=tool_calls
            ))
            for tool_call in tool_calls:
                function_call = tool_call['function']
                match function_call['name']:
                    case "internet_query":
                        args = InternetQueryArgs.model_validate_json(function_call['arguments'])
                        result = await internet_query(args)
                    case "search":
                        args = SearchArgs.model_validate_json(function_call['arguments'])
                        result = await search(args)
                new_messages.append(ChatMessage(
                    role="tool",
                    tool_call_id=tool_call['id'],
                    content=result
                ))
                yield WSResponse(
                    kind="tool_result",
                    tool_call_id=tool_call['id'],
                    content=result
                )
            chat_messages.extend(msg.model_dump() for msg in new_messages)
            logger.info(f"Chat messages for continuation: {chat_messages}")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                tools=tools,
                tool_choice="auto",
                stream=True
            )
        yield WSResponse(kind="done")
        logger.info(f"Raising StopAsyncGenerator with messages: {new_messages}")
        raise StopAsyncGenerator(new_messages)
