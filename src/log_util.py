
import logging
from logging.config import dictConfig

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
LOG_LEVEL = logging.INFO

LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=True,
    formatters={
        'standard': {
            'format': LOG_FORMAT
        },
    },
    handlers={
        'default': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    loggers={
        '': {
            'handlers': ['default'],
            'level': LOG_LEVEL, # only log entries this level and above will be included
            'propagate': False
        }
    }
)

def get_logger(logger_name: str, logging_config: dict = LOGGING_CONFIG) -> logging.Logger:
    dictConfig(logging_config)
    return logging.getLogger(logger_name)
