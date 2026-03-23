from base64 import b64encode
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.teamup.domain import Response, UserGames
from src.teamup.infra import (
    GameRepository,
    ResponseRepository,
    UserGamesRepository,
    UserRepository,
)
from src.teamup.schemas import TokenData

from ..di import get_current_user

wrapper_router = APIRouter(tags=["User Activity"])


async def _check_user(user_id: UUID):
    async with UserRepository() as repo:
        user = await repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=403, detail="Пользователь не найден")


@wrapper_router.post("/a/{announcement_id}/responses/new")
async def create_response(
    announcement_id: UUID, user: TokenData = Depends(get_current_user)
):
    response = Response(
        user_id=user.user_id,
        announcement_id=announcement_id,
    )

    async with ResponseRepository() as repo:
        res = await repo.create(response)
        if res is None:
            raise HTTPException(status_code=400, detail="Не удалось создать запрос")

        return {
            "user_id": res.user_id,
            "announcement_id": res.announcement_id,
            "status": res.status,
            "created_at": res.created_at,
            "updated_at": res.updated_at,
        }


@wrapper_router.get("/a/{announcement_id}/responses/")
async def get_responses_in_announcement(
    announcement_id: UUID,
    user: TokenData = Depends(get_current_user),
):
    await _check_user(user.user_id)

    async with ResponseRepository() as repo:
        res = await repo.get_by_announcement(announcement_id)
        if res is None:
            raise HTTPException(status_code=404, detail="Запрос не найден")
        return [
            {
                "response_id": r.response_id,
                "user_id": r.user_id,
                "announcement_id": r.announcement_id,
                "status": r.status,
                "created_at": r.created_at,
            }
            for r in res
        ]


@wrapper_router.get("/games")
async def get_all_games(user: TokenData = Depends(get_current_user)):
    await _check_user(user.user_id)
    async with GameRepository() as repo:
        res = await repo.get_all()
        res_ = map(
            lambda x: {
                "game_id": x.game_id,
                "game_name": x.game_name,
                "game_icon": b64encode(x.game_icon).decode(),
            },
            res,
        )
        return list(res_)


@wrapper_router.get("/games/{game_id}")
async def get_game(
    game_id: UUID,
    user: TokenData = Depends(get_current_user),
):
    await _check_user(user.user_id)

    async with GameRepository() as repo:
        res = await repo.get_by_id(game_id)
        if res is None:
            raise HTTPException(status_code=404, detail="Игра не найдена")
        return {
            "game_id": res.game_id,
            "game_name": res.game_name,
            "game_icon": b64encode(res.game_icon).decode(),
        }


@wrapper_router.get("/games/{game_id}/add")
async def add_game(
    game_id: UUID,
    user: TokenData = Depends(get_current_user),
):
    await _check_user(user.user_id)
    ug = UserGames(user_id=user.user_id, game_id=game_id)
    async with UserGamesRepository() as repo:
        res = await repo.create(ug)
        if res is None:
            raise HTTPException(status_code=404, detail="Не удалось добавить игру")
        return {"user_id": user, "game_id": game_id, "preferred": res.preferred}
