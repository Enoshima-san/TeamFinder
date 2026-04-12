class ResponseException(Exception):
    """Базовое исключение для запросов в объялвениях"""

    pass


class ResponseCreationError(ResponseException):
    """Ошибка при создании запроса"""

    pass


class ResponseNotFoundError(ResponseException):
    """Ошибка при получении запроса"""

    pass


class ResponseDeletionError(ResponseException):
    """Ошибка при удалении запроса"""

    pass
