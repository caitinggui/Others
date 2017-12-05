# -*- coding: utf-8 -*-

import time
import signal
import sys
import logging
import functools
from threading import Thread

from exceptions import RuntimeError
logging.basicConfig(level=logging.DEBUG)


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


def ensureDone(times):
    """执行函数times次，直到函数运行成功,否则引发Exception异常。一定要在所有装饰器的最外层！"""
    logger = logging.getLogger(__name__)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            for i in xrange(times):
                try:
                    result = func(*args, **kw)
                    return result
                except Exception as e:
                    logger.warn("execute func: %s fail for %s times: %s",
                                func.__name__, i, e, exc_info=True)
            raise Exception(e)
        return wrapper
    return decorator


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

    @ensureDone(3)
    @setTimeout(5)
    @showTicker
    def test():
        print "func start"
        time.sleep(3)
        print "func continue"
        time.sleep(6)
        # 不会打印这一段，说明函数被终止执行
        print "func end"
        return 'test OK'

    @ensureDone(3)
    @setTimeout(3)
    def test2():
        print 'test2 start'
        time.sleep(1)
        print "test2 end"

    try:
        print test()
    except RuntimeError as e:
        print "test func abort: ", e
    test2()
    time.sleep(10)
