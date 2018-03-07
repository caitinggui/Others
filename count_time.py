# coding: utf-8

import time
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Timer(object):

    def __init__(self, name=''):
        self.name = name
        self.start = time.time()
        self.end = None
        self.cost = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.end = time.time()
        self.cost = self.end - self.start
        logger.info("%s time cost: %s", self.name, self.cost)
        return self.cost


if __name__ == "__main__":
    with Timer(time.sleep) as timer:
        time.sleep(1)
    print(timer.cost)
    with Timer() as _:
        time.sleep(3)
