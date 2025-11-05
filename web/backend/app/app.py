import fastapi
import os
from api import api

try:
    from web.backend.app.llm import LLM
except ImportError:
    from llm import LLM

LLM_HOST = os.getenv("LLM_HOST", "localhost")
LLM_PORT = os.getenv("LLM_PORT", "11434")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")


async def lifespan(app: fastapi.FastAPI):
    app.state.llm = LLM(
        url=f"http://{LLM_HOST}:{LLM_PORT}/v1",
        model=LLM_MODEL,
        api_key=LLM_API_KEY
    )
    yield
    app.state.llm = None


app = fastapi.FastAPI(lifespan=lifespan, docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json")
app.include_router(api, prefix="/api")