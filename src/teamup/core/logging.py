import inspect
import logging
import sys

from colorama import Fore, Style, init

init(autoreset=True)


class ColorFormatter(logging.Formatter):
    """
    Кастомный форматтер для добавления цветов в логи.
    """

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        # Сохраняем оригинальные цвета, чтобы не ломать другие хендлеры
        orig_levelname = record.levelname
        orig_name = record.name

        # Применяем цвет к уровню
        color = self.COLORS.get(record.levelno, "")
        record.levelname = f"{color}{orig_levelname}{Style.RESET_ALL}"

        # Применяем голубой цвет к имени модуля (пути)
        record.name = f"{Fore.BLUE}{orig_name}{Style.RESET_ALL}"

        # Форматируем запись
        result = super().format(record)

        # Восстанавливаем оригинальные значения (хорошая практика)
        record.levelname = orig_levelname
        record.name = orig_name

        return result


def setup_logging(level=logging.INFO):
    """
    Единая настройка форматирования и хендлеров с поддержкой цветов.
    Вызывается один раз при старте приложения.
    """
    if not logging.root.handlers:  # избегаем дублирования хендлеров
        handler = logging.StreamHandler(sys.stdout)

        # Создаем наш цветной форматтер
        formatter = ColorFormatter(
            "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s |",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        handler.setFormatter(formatter)
        logging.root.addHandler(handler)
        logging.root.setLevel(level)


def get_logger(name=None):
    """
    Фабрика логгеров.
    Если name не указан — автоматически определяет имя вызывающего модуля.
    """
    if name is None:
        frame = inspect.currentframe().f_back  # type: ignore[reportOptionalMemberAccess]
        name = frame.f_globals.get("__name__", "root")  # type: ignore[reportOptionalMemberAccess]

    logger = logging.getLogger(name)
    return logger
