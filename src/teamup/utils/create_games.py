import asyncio
import io
from pathlib import Path
from uuid import UUID

from PIL import Image

from teamup.core.di import get_game_repository
from teamup.domain import Game
from teamup.infra.database import get_async_session

IMAGES_DIR = Path(__file__).resolve().parent / "images"

def image_to_bytes(image_name: str) -> bytes:
    image_path = IMAGES_DIR / image_name
    if not image_path.exists():
        raise FileNotFoundError(f"Изображение не найдено: {image_path}")

    with Image.open(image_path) as img:
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        return buffer.getvalue()

GAMES_CONFIG = [
    {
        "game_id": UUID("00000000-0000-0000-0000-000000000000"),
        "game_name": "Dota 2",
        "img": "dota.jpg",
    },
    {
        "game_id": UUID("00000000-0000-0000-0000-000000000001"),
        "game_name": "CS GO",
        "img": "cs.jpg",
    },
    {
        "game_id": UUID("00000000-0000-0000-0000-000000000002"),
        "game_name": "LoL",
        "img": "lol.png",
    },
    {
        "game_id": UUID("00000000-0000-0000-0000-000000000003"),
        "game_name": "WoW",
        "img": "wow.png",
    },
]

async def create():
    session_gen = get_async_session()
    try:
        db = await session_gen.__anext__()
        repo = await get_game_repository(db)

        for cfg in GAMES_CONFIG:
            game_data = {
                "game_id": cfg["game_id"],
                "game_name": cfg["game_name"],
                "game_icon": image_to_bytes(cfg["img"]),
            }
            await repo.create(Game(**game_data))

        await db.commit()
        print("Games created successfully.")
    except Exception as e:
        print(f"Error: {e}")
        await db.rollback()
    finally:
        await session_gen.aclose()

if __name__ == "__main__":
    asyncio.run(create())