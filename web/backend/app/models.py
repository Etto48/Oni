import pydantic
from typing import Literal


class ChatCommand(pydantic.BaseModel):
    kind: Literal["stop", "message", "restore"]

class ChatMessage(ChatCommand):
    kind: Literal["message"] = "message"
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRestore(ChatCommand):
    kind: Literal["restore"] = "restore"
    messages: list[ChatMessage]

class ChatStop(ChatCommand):
    kind: Literal["stop"] = "stop"

class WSResponse(pydantic.BaseModel):
    kind: Literal["text", "done"]

class WSResponseText(WSResponse):
    kind: Literal["text"] = "text"
    text: str

class WSResponseDone(WSResponse):
    kind: Literal["done"] = "done"