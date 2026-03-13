from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from starlette.middleware.cors import CORSMiddleware

from .api import (
    auth_router,
    get_current_user,
    get_user_repository,
)
from .application import IUserRepository
from .core import logger
from .infra import check_database_connection
from .schemas import TokenData, UserResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_database_connection()
    logger.info("Подключение к базе данных удалось")
    yield
    # Perform any necessary cleanup or teardown here


app = FastAPI()

app.include_router(auth_router, prefix="/auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {
        "head": "TeamUP",
        "message": "find ur femboy",
        "docs": "http://localhost:8000/docs",
    }


@app.get("/users/me", response_model=UserResponse)
async def get_current_user_info(
    curr_user: TokenData = Depends(get_current_user),
    user_repository: IUserRepository = Depends(get_user_repository),
):
    user = await user_repository.get_by_id(curr_user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return UserResponse(
        username=user.username,
        email=user.email,
        registration_date=user.registration_date,
        age=user.age,
        about_me=user.about_me,
    )


@app.get("/protected")
async def protected_resource(current_user: TokenData = Depends(get_current_user)):
    """Тестовый Эндпоинт"""
    return {
        "message": f"Hello, {current_user.username}!",
        "user_id": str(current_user.user_id),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.teamup.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # ← автоперезагрузка
        reload_dirs=["src/teamup"],  # ← какие папки отслеживать
        log_level="info",
    )
