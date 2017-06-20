#!/usr/bin/env python
# codit: utf-8

import logging

# basic usage
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
    filename='blog.log')

logger = logging.getLogger(__name__)
logger.info("This is basic usage of logging")

# advanced usage
logger = logging.getLogger('mylog')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s%(name)s[line:%(lineno)d]%(levelname)s-%(message)s')
logfile = logging.FileHandler("./log.txt")
console = logging.StreamHandler()
logfile.setLevel(logging.ERROR)
console.setLevel(logging.DEBUG)
logfile.setFormatter(formatter)

logger.addHandler(logfile)
logger.addHandler(console)

logger.info('It will only log to console')
logger.error('It will log to console and file')


# dict usage
import logging.config

log_setting = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "formatter": "detail",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG"
        },
        "file": {
            "formatter": "standard",
            "filename": "log.log",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG"
        },
        "socket": {
            "level": "DEBUG",
            "class": "logging.handlers.SocketHandler",
            "host": "127.0.0.1",
            "port": 8002,
            "formatter": "standard"
        },
        "http": {
            "level": "DEBUG",
            "class": "logging.handlers.HTTPHandler",
            "host": "127.0.0.1",
            "url": "/log",
            "method": "POST",
            "formatter": "standard"
        },
        "mail": {
            "level": "DEBUG",
            "class": "logging.handlers.SMTPHandler",
            "mailhost": "",
            "fromaddr": "",
            "toaddrs": "",
            "subject": "",
            "credentials": "",
            "formatter": "standard"
        }
    },
    "formatters": {
        "simple": {
            "format": "%(filename)s[line:%(lineno)d]%(levelname)s %(message)s"
        },
        "detail": {
            "format": "%(asctime)s %(filename)s[line:%(lineno)d]%(name)s %(levelname)s %(message)s"
        },
        "standard": {
            "format": "%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s-%(message)s"
        }
    },
    "root": {
        "level": "WARN",
        "propagate": False,
        "handlers": ["console", "file"]
    },
    "loggers": {
        "web": {
            "handlers": ["console", "file"],
            "propagate": False,
            "level": "DEBUG"
        }
    }
}
logging.config.dictConfig(log_setting)

logger = logging.getLogger('web')
logger.info('Hello world')


