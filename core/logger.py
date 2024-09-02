import logging 
import sys 
import os 
from pathlib import Path 
from loguru import logger

from core.config import configs

class InterceptHandler(logging.Handler):
    """logging의 핸들러를 loguru에 적용시키는 클래스"""
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        msg = record.getMessage()
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = logging.currentframe(), 2
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, msg)

class CustomLogger:
    """loguru logger를 커스텀하는 메서드"""
    def __init__(self):
        self.logger = logger 

        self.formatter = "<lvl>{level: <8}</lvl> <g>{time:YYYY-MM-DD HH:mm:ss.SSS}</g> <c>{name}</c>:<c>{function}</c> - <lvl>{message}</lvl>"

        self._customize_logger()

    def _customize_logger(self):
        self.logger.remove()

        self.logger.add(
            sys.stderr,
            enqueue=True,
            format=self.formatter,
            level="INFO"
        )

        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


custom_logger = CustomLogger()
logger = custom_logger.logger