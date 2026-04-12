class AuthException(Exception):
    """Базовое исключение для авторизации"""

    pass


class UserAlreadyExistsError(AuthException):
    """Пользователь с таким email или username уже существует"""

    pass


class UserCreationError(AuthException):
    """Ошибка при создании пользователя"""

    pass


class PermissionDeniedError(AuthException):
    """Пользователь не найден"""

    pass


class InvalidCredentialsError(AuthException):
    """Неверные учётные данные (пароль не совпадает)"""

    pass


class InvalidTokenError(AuthException):
    """Токен невалиден или истёк"""

    pass


class PasswordMismatchError(AuthException):
    """Пароль не совпадает"""

    pass
