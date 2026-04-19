from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import (
    auth_router,
    chat_router,
    chat_ws_router,
    exception_handler,
    external_router,
    feed_router,
    games_router,
    user_router,
)
from .application.exceptions import (
    AnnouncementException,
    AuthException,
    ExternalApiException,
    ResponseException,
    UseCasesException,
)
from .core import get_logger
from .core.di import get_current_user
from .infra import check_database_connection
from .schemas import TokenData

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_database_connection()
    logger.info("Подключение к базе данных удалось")
    yield
    # Perform any necessary cleanup or teardown here


app = FastAPI()

app.include_router(auth_router)
app.include_router(feed_router)
app.include_router(games_router)
app.include_router(external_router)
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(chat_ws_router)

app.add_exception_handler(AnnouncementException, exception_handler)
app.add_exception_handler(AuthException, exception_handler)
app.add_exception_handler(UseCasesException, exception_handler)
app.add_exception_handler(ExternalApiException, exception_handler)
app.add_exception_handler(ResponseException, exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://ff08xs96-8000.euw.devtunnels.ms",
        "null"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


@app.get("/info")
async def info():
    return {
        "head": "TeamUP",
        "message": "find ur femboy",
        "docs": "http://localhost:8000/docs",
    }


@app.get("/protected")
async def protected_resource(current_user: TokenData = Depends(get_current_user)):
    """Тестовый Эндпоинт"""
    return {
        "message": f"Hello, {current_user.username}!",
        "user_id": str(current_user.user_id),
    }


def start():
    import uvicorn

    uvicorn.run(
        "teamup.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["teamup"],
        log_level="info",
    )


if __name__ == "__main__":
    start()
