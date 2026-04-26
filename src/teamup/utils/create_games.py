import asyncio
import io
from pathlib import Path
from uuid import UUID

from PIL import Image

from teamup.core.di import get_game_repository
from teamup.domain import Game
from teamup.infra.database import get_async_session

BASE_DIR = Path(__file__).parent


def image_to_bytes(image_path: str) -> bytes:
    full_path = BASE_DIR / image_path
    with Image.open(full_path) as img:
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        return img_bytes.getvalue()


games = [
    {
        "game_id": UUID("00000000-0000-0000-0000-000000000000"),
        "game_name": "Dota 2",
        "game_icon": "1234",
    },
    {
        "game_id": UUID("00000000-0000-0000-0000-000000000001"),
        "game_name": "CS GO",
        "game_icon": "1234",
    },
    {
        "game_id": UUID("00000000-0000-0000-0000-000000000002"),
        "game_name": "LoL",
        "game_icon": "1234",
    },
    {
        "game_id": UUID("00000000-0000-0000-0000-000000000003"),
        "game_name": "WoW",
        "game_icon": "1234",
    },
]


async def create():
    session = get_async_session()
    db = await session.__anext__()
    repo = await get_game_repository(db)
    [await repo.create(Game(**game)) for game in games]
    await db.commit()


def run():
    asyncio.run(create())
