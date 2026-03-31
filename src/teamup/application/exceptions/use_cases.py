class UseCasesException(Exception):
    """Базовое исключение для UseCases"""

    ...


class UserNotFoundError(UseCasesException):  # 404
    """Исключение, возникающее при попытке получить несуществующего пользователя"""

    ...


class UserGameCreationError(UseCasesException):  # 400
    """Исключение, возникающее при попытке создать игру для пользователя"""

    ...
