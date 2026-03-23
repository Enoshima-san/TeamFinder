import io
from pathlib import Path

from PIL import Image

from src.teamup.core import get_logger
from src.teamup.domain import Game

from ...di import get_game_repository

base_path = Path(__file__).parent
logger = get_logger()


def image_to_bytes(image_path: str) -> bytes:
    """Конвертирует изображение в bytes"""
    img_path = base_path / image_path
    with Image.open(img_path) as img:
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        return img_bytes.getvalue()


games = [
    {
        "game_name": "Dota 2",
        "game_icon": image_to_bytes("dota.png"),
    },
    {
        "game_name": "Counter-Strike",
        "game_icon": image_to_bytes("cs.png"),
    },
]


async def create():
    async with await get_game_repository() as repo:
        _games = [Game.create(**g) for g in games]
        cnt = 0

        for g in _games:
            game = await repo.create(g)
            if game is None:
                cnt += 1
                logger.error(f"Создание игры {g.game_name} не удалось")

        assert cnt == 0, f"Не удалось создать {cnt} игр"


if __name__ == "__main__":
    import asyncio

    asyncio.run(create())
