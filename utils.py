import threading
import random


def set_timeout(fn, delay, args = None, kwargs = None):
    t = threading.Timer(delay, fn, args, kwargs)
    t.start()
