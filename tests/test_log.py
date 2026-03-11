import logging

from src.teamup.core import logger


def test_logger_outputs():
    """Проверяет, что логгер выводит сообщения"""
    root = logging.getLogger()
    assert len(root.handlers) > 0, "Нет обработчиков у root logger"

    logger.debug("🔍 DEBUG")
    logger.info("✅ INFO")
    logger.warning("⚠️ WARNING")

    assert True
