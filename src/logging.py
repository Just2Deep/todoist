import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FORMAT_INFO = "%(asctime)s - %(levelname)s - %(message)s"

class LogLevels(StrEnum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"

def configure_logging(level: LogLevels = LogLevels.error) -> None:
    """
    Configure the logging settings for the application.

    Args:
        level (LogLevels): The logging level to set.
    """
    log_level = str(level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(
            level=LogLevels.error,
        )

        return

    if log_level == LogLevels.debug:
        logging.basicConfig(
            level=level.value,
            format=LOG_FORMAT_DEBUG,
        )

        return 
    
    logging.basicConfig(
        level=level.value
    )