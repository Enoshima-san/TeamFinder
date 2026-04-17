class UseCasesException(Exception):
    """Базовое исключение для UseCases"""

    ...


class UserNotFoundError(UseCasesException):  # 404
    """Исключение, возникающее при попытке получить несуществующего пользователя"""

    ...


class UserGameCreationError(UseCasesException):  # 400
    """Исключение, возникающее при попытке создать игру для пользователя"""

    ...


class ConversationCreationError(UseCasesException):  # 400
    """Исключение, возникающее при попытке создать диалог после запроса"""

    ...


class MessageCreationError(UseCasesException):  # 403
    """Исключение, возникающее при попытке отправить сообщение пользователю"""

    ...


class ConversationNotFoundError(UseCasesException):  # 404
    """Исключение, возникающее при попытке получить несуществующий диалог"""

    ...


class ConversationBadRequestError(UseCasesException):  # 400
    ...
