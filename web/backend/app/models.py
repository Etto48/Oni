import pydantic
from typing import Literal

class ChatMessage(pydantic.BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    tool_calls: list[dict] = []
    tool_call_id: str | None = None
    content: str = ""

class ChatCommand(pydantic.BaseModel):
    kind: Literal["stop", "message", "restore"]
    message: ChatMessage | None = None
    messages: list[ChatMessage] | None = None

class WSResponse(pydantic.BaseModel):
    kind: Literal["text", "reasoning", "done", "tool_calls", "tool_result"]
    text: str | None = None
    reasoning: str | None = None
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None
    content: str | None = None

class StopAsyncGenerator(Exception):
    def __init__(self, value):
        self.value = value