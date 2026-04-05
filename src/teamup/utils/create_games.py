import asyncio
import io
import uuid
from pathlib import Path

from PIL import Image

from teamup.api.di import get_game_repository
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
        "game_id": uuid.uuid4(),
        "game_name": "Dota 2",
        "game_icon": image_to_bytes("images/dota.jpg"),
    },
    {
        "game_id": uuid.uuid4(),
        "game_name": "Counter-Strike",
        "game_icon": image_to_bytes("images/cs.jpg"),
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
