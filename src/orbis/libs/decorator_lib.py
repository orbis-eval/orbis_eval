#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-



import functools
import time
import os
import json

from orbis.config import paths


def timed(app):
    """

    :return:
    """
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            start = time.time()
            result = fn(*args, **kwargs)
            duration = time.time() - start
            app.logger.info(repr(fn), duration * 1000)
            return result
        return inner
    return decorator


def save_as_json(file_name):
    """

    :param file_name:
    :return:
    """
    def decorator(func):
        """

        :param func:
        :return:
        """
        @functools.wraps(func)
        def inner(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            file_path = os.path.abspath(os.path.join(os.path.join(paths.data_dir)))
            result = func(*args, **kwargs)
            with open(os.path.join(file_path, "{}.json".format(file_name)), "w") as open_file:
                json.dump(result, open_file, separators=(',', ':'), indent=2)
            return result
        return inner
    return decorator
