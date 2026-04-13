from fastapi import APIRouter

from ..di import get_top_players_use_case

external_router = APIRouter(tags=["External"], prefix="/api/external")


@external_router.get("/cyber-sport-ru/{game_name}")
async def get_top_players(
    game_name: str,
):
    """
    Возвращает топ игроков для указанной игры.
    """
    tp_us = await get_top_players_use_case(game_name)
    res = await tp_us()
    return res
