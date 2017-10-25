# -*- coding: utf-8 -*-

import time
import signal
import sys
import logging
import functools
from threading import Thread

from exceptions import RuntimeError


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


def showTicker(func):
    class Ticker(object):
        def __init__(self):
            self.tick = True

        def show(self):
            sys.stdout.write('.')
            sys.stdout.flush()

        def run(self):
            while self.tick:
                self.show()
                time.sleep(1)

    @functools.wraps(func)
    def wrapper(*args, **kw):
        ticker = Ticker()
        Thread(target=ticker.run).start()
        try:
            result = func(*args, **kw)
        # 保证ticker被关掉
        finally:
            ticker.tick = False
        return result
    return wrapper


def setTimeout(runtime):
    def handle(signum, frame):
        raise RuntimeError("Out of runtime!")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            signal.signal(signal.SIGALRM, handle)
            signal.alarm(runtime)  # 开启闹钟信号
            try:
                result = func(*args, **kw)
            finally:
                signal.alarm(0)  # 关闭闹钟信号
            return result
        return wrapper
    return decorator


if __name__ == "__main__":

    @setTimeout(5)
    @showTicker
    def test():
        print "func start"
        time.sleep(3)
        print "func continue"
        time.sleep(6)
        print "func end"

    @setTimeout(3)
    def test2():
        print 'test2 start'
        time.sleep(1)
        print "test2 end"

    try:
        test()
    except RuntimeError as e:
        print "test func abort: ", e
    test2()
