import logging, sys
from typing import Literal


def GetLogger(name: str, level: Literal[0]) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = ColoredFormatter(
        "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[91m",  # Red
        "RESET": "\033[0m",  # Reset to default color
    }

    def format(self, record):
        log_message = super().format(record)
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        return f"{color}{log_message}{self.COLORS['RESET']}"