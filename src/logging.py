import enum, sys
from loguru import logger


class LoggingLevel(enum.Enum):
    """Enum for logging levels."""

    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    def to_int(self) -> int:
        return {
            LoggingLevel.TRACE: 5,
            LoggingLevel.DEBUG: 10,
            LoggingLevel.INFO: 20,
            LoggingLevel.SUCCESS: 25,
            LoggingLevel.WARNING: 30,
            LoggingLevel.ERROR: 40,
            LoggingLevel.CRITICAL: 50,
        }[self]


def setup_logging(logging_level: LoggingLevel) -> None:
    """Setup logging for the addon."""
    logger.remove()
    if logging_level.to_int() < LoggingLevel.WARNING.to_int():
        logger.add(
            sys.stdout,
            level=logging_level.to_int(),
            filter=lambda record: record["level"].no < LoggingLevel.WARNING.to_int(),
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
    logger.add(
        sys.stderr,
        level=logging_level.to_int(),
        filter=lambda record: record["level"].no >= LoggingLevel.WARNING.to_int(),
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    logger.debug("Logging was setup!")
