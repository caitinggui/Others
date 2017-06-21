# -*- coding: utf-8 -*-

import time
import logging
import functools
from threading import Thread


def runTime(func):
    logger = logging.getLogger('web')

    @functools.wraps(func)
    def wrapper(*args, **kw):
        time1 = time.time()
        result = func(*args, **kw)
        run_time = time.time() - time1
        logger.info('%s run time: %f' % (func.__name__, run_time))
        return result
    return wrapper


def asyncFunc(func):
    logger = logging.getLogger('web')

    @functools.wraps(func)
    def wrapper(*args, **kw):
        thr = Thread(target=func, args=args, kwargs=kw)
        logger.info('Thread %s start!', func.__name__)
        thr.start()
    return wrapper
