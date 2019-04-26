from ar.config import *
import logging.config
import logging


MY_LOGGINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s:%(module)s:%(funcName)s:%(lineno)d - %(levelname)s - %(process)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": f"/var/log/ampos/{CONTAINER_TAG}.log" if CONTAINER_TAG else "/var/log/ampos/app.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 3,
            "encoding": 'utf-8',  # if not set to 'utf-8', Unicode char will fail to log
            "delay": False,
            "utc": False,
            "atTime": None
        },
    },
    "loggers": {
        '': {  # root logger
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        "ar": {
            "level": "DEBUG",
            # "handlers": ['console', 'file']
            "propagate": True
        }
    },
}

logging.config.dictConfig(MY_LOGGINGS)
