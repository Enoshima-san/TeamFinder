class AnnouncementException(Exception):
    """Базовое исключение для объявлений"""

    pass


class AnnouncementNotFoundError(AnnouncementException):
    """Объявление не найдено"""

    pass


class AnnouncementCreationError(AnnouncementException):
    """Ошибка при создании объявления"""

    pass


class AnnouncementDeleteError(AnnouncementException):
    """Ошибка при удалении объявления"""

    pass


class AnnouncementUpdateError(AnnouncementException):
    """Ошибка при обновлении объявления"""

    pass


class InvalidRankRangeError(AnnouncementException):
    """Некорректный диапазон рангов"""

    pass


class GameNotFoundError(AnnouncementException):
    """Игра не найдена"""

    pass


class UnauthorizedError(AnnouncementException):
    """Нет прав на операцию"""

    pass


class ForbiddenError(AnnouncementException):
    """Доступ запрещён"""

    pass
