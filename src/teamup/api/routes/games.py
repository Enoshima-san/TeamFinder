from uuid import UUID

from fastapi import APIRouter, Depends

from teamup.application.di import get_add_game_use_case, get_games_service
from teamup.application.services import GamesService
from teamup.application.use_cases import AddGameUseCase
from teamup.core.di import get_current_user
from teamup.schemas import GameResponse, TokenData

games_router = APIRouter(tags=["Games"], prefix="/games")


@games_router.get("/", response_model=list[GameResponse])
async def get_all_games(
    games_s: GamesService = Depends(get_games_service),
):
    games = await games_s.get_all_games()
    res = [GameResponse.create(g) for g in games]
    return res


@games_router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: UUID,
    games_s: GamesService = Depends(get_games_service),
):
    game = await games_s.get_game_by_id(game_id)
    res = GameResponse.create(game)
    return res


@games_router.get("/{game_id}/add")
async def add_game(
    game_id: UUID,
    ag_uc: AddGameUseCase = Depends(get_add_game_use_case),
    token_data: TokenData = Depends(get_current_user),
):
    res = await ag_uc(token_data.user_id, game_id)
    return res
