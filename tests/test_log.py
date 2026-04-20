import logging

from teamup.core import get_logger

logger = get_logger()


def test_logger_outputs():
    """Проверяет, что логгер выводит сообщения"""
    root = logging.getLogger()
    assert len(root.handlers) > 0, "Нет обработчиков у root logger"
    print()
    logger.debug("🔍 DEBUG")
    logger.info("✅ INFO")
    logger.warning("⚠️ WARNING")

    assert True
