# -*- coding: utf-8 -*-

import functools
import json
import os
import time

import logging
logger = logging.getLogger(__name__)

from orbis_eval.config import paths

# wip
def capture_io():
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            result = fn(*args, **kwargs)

            return result
        return inner
    return decorator


def clear_screen():
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            if logger.level != "debug":
                os.system('cls')  # on Windows
                os.system('clear')  # on linux / os x

            result = fn(*args, **kwargs)
            return result
        return inner
    return decorator


def timed():
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            start = time.time()
            result = fn(*args, **kwargs)
            duration = time.time() - start
            logger.info(repr(fn), duration * 1000)
            return result
        return inner
    return decorator


def save_as_json(file_name):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            file_path = os.path.abspath(os.path.join(os.path.join(paths.data_dir)))
            result = func(*args, **kwargs)
            with open(os.path.join(file_path, "{}.json".format(file_name)), "w") as open_file:
                json.dump(result, open_file, separators=(',', ':'), indent=2)
            return result
        return inner
    return decorator


def query(app):
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            try:
                result = fn(*args, **kwargs)
            except Exception as exception:
                logger.error(f"Query failed: {exception}")
                result = None
            return result
        return inner
    return decorator
