#!/usr/bin/env python
# coding: utf-8

import signal
import time
import functools

from exceptions import RuntimeError


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


if __name__ == '__main__':

    @setTimeout(4)
    def getName():
        while True:
            print 'TT'
            time.sleep(1)
        return

    try:
        s = getName()
    except RuntimeError as e:
        print e
    else:
        print s
    print "i can still run"
