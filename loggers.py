#!/usr/bin/env python
# coding: utf-8

"""
在多进程下只能使用 multiprocessfile，否则可能导致日志丢失、错乱.
需要安装 pip install ConcurrentLogHandler
"""

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
        "rotatingfile": {
            "formatter": "standard",
            "filename": "log.log",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "maxBytes": 1024 * 1024 * 100,  # 单位为字节，这里为100MB
            "backupCount": 60                 # 保留60份
        },
        "timefile": {
            "formatter": "standard",
            "filename": "log.log",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "interval": 1,
            "when": "midnight",     # 半夜时切分文件,h-小时, s-秒, m-分, d-天, w2-周二
            "backupCount": 60         # 保留60份
        },
        "multiprocessfile": {  # 支持多进程下使用，其他handler不支持多进程
            'formatter': 'standard',
            "filename": "log.log",
            # 如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失
            # pip install ConcurrentLogHandler==0.9.1
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            # 当达到100MB时分割日志
            'maxBytes': 1024 * 1024 * 100,
            # 最多保留50份文件
            'backupCount': 50,
            'level': 'DEBUG',
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
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
            "format": "%(asctime)s %(filename)s[line:%(lineno)d]%(name)s %(levelname)s %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        "standard": {
            "format": "%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s-%(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        }
    },
    "root": {
        "level": "WARN",
        "propagate": False,
        "handlers": ["console", "rotatingfile"]
    },
    "loggers": {
        "web": {
            "handlers": ["console", "timefile", "multiprocessfile"],
            "propagate": False,
            "level": "DEBUG"
        }
    }
}
logging.config.dictConfig(log_setting)

logger = logging.getLogger('web')
logger.info('Hello world')


try:
    raise KeyError("None Key")
except KeyError as e:
    logger.info('---------exception----------')
    logger.exception(e)
    logger.info('---------error----------')
    logger.error(e)
    logger.info('---------error with exc_info----------')
    logger.info(e, exc_info=True)
