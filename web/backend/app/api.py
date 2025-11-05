import asyncio
import fastapi
from models import ChatCommand, ChatMessage, ChatRestore, WSResponse, WSResponseDone, WSResponseText
import logging
try:
    from web.backend.app.llm import LLM
except ImportError:
    from llm import LLM
logger = logging.getLogger("api")

api = fastapi.APIRouter()

@api.get("/health")
async def health_check():
    return {"status": "ok"}

@api.websocket("/chat")
async def chat_completion(websocket: fastapi.WebSocket):
    await websocket.accept()
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant. You can use appropriate tools to answer user queries.")
    ]
    llm: LLM = websocket.app.state.llm
    async def try_receive():
        return ChatCommand(**await websocket.receive_json())
    try:
        while True:
            command_dict = await websocket.receive_json()
            command = ChatCommand(**command_dict)
            match command.kind:
                case "message":
                    messages.append(ChatMessage(**command_dict))
                    response_stream = llm.chat_completion(messages)
                    new_message = ChatMessage(role="assistant", content="")
                    async for chunk in response_stream:
                        recv_task = asyncio.create_task(try_receive())
                        try:
                            command = await asyncio.wait_for(recv_task, timeout=0.1)
                            if command.kind == "stop":
                                logger.info("Received stop command from client.")
                                break
                        except asyncio.TimeoutError:
                            pass

                        new_message.content += chunk
                        await websocket.send_json(WSResponseText(text=chunk).model_dump())
                    messages.append(new_message)
                    await websocket.send_json(WSResponseDone().model_dump())
                case "restore":
                    restore = ChatRestore(**command_dict)
                    messages = restore.messages
                case _:
                    pass
    except fastapi.WebSocketDisconnect:
        pass
