#!/usr/bin/env python

import sys
import threading
import time


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


ticker = Ticker()
threading.Thread(target=ticker.run).start()
raw_input()
ticker.tick = False
