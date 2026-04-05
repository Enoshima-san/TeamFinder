from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application.check_rules import get_game_or_fail, get_user_or_fail
from teamup.infra.database import get_async_session
from teamup.schemas import GameResponse, TokenData

from ..di import get_add_game_use_case, get_current_user, get_games_service

games_router = APIRouter(tags=["Games"], prefix="/games")


@games_router.get("/", response_model=list[GameResponse])
async def get_all_games(
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    await get_user_or_fail(db, token_data.user_id)
    games_s = await get_games_service(db)
    games = await games_s.get_all_games()
    res = [GameResponse.create(g) for g in games]
    return res


@games_router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    await get_user_or_fail(db, token_data.user_id)
    games_s = await get_games_service(db)
    game = await games_s.get_game_by_id(game_id)
    res = GameResponse.create(game)
    return res


@games_router.get("/{game_id}/add")
async def add_game(
    game_id: UUID,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    await get_user_or_fail(db, token_data.user_id)
    await get_game_or_fail(db, game_id)
    ag_uc = await get_add_game_use_case(db)
    res = await ag_uc(token_data.user_id, game_id)
    await db.commit()
    return res
