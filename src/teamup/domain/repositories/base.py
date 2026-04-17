from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from teamup.core import get_logger


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        self.logger = get_logger()
        self.session = session
