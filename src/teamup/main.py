```python
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
async def database_lifespan(app: FastAPI):
    """
    Context manager to ensure database connection is established before app startup.
    
    Args:
    app (FastAPI): The FastAPI application instance.
    """
    await check_database_connection()
    logger.info("Database connection established successfully")
    yield
    # Perform any necessary cleanup or teardown here


def create_fastapi_app() -> FastAPI:
    """
    Creates a FastAPI application instance with necessary middleware and routes.
    
    Returns:
    FastAPI: The created FastAPI application instance.
    """
    app = FastAPI()

    app.include_router(auth_router, prefix="/auth")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def main():
    app = create_fastapi_app()

    @app.get("/")
    async def root():
        """
        Returns a simple "Hello World" response.
        
        Returns:
        dict: A dictionary containing a greeting message.
        """
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
        """
        Retrieves the current user's information.
        
        Args:
        curr_user (TokenData): The current user's token data.
        user_repository (IUserRepository): The user repository instance.
        
        Returns:
        UserResponse: The current user's information.
        
        Raises:
        HTTPException: If the user is not found.
        """
        user = await user_repository.get_by_id(curr_user.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
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
        """
        A protected endpoint that returns a personalized message.
        
        Args:
        current_user (TokenData): The current user's token data.
        
        Returns:
        dict: A dictionary containing a personalized message.
        """
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
            reload=True,
            reload_dirs=["src/teamup"],
            log_level="info",
        )


if __name__ == "__main__":
    main()
```