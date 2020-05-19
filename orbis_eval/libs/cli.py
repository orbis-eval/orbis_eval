# -*- coding: utf-8 -*-

from pprint import pformat
import functools
import time

from orbis_eval.core import app
import logging
logger = logging.getLogger(__name__)


def multiline_logging(msg, level=None):

    try:
        msg = msg.decode("utf-8")
    except Exception:
        pass

    msg = str(msg)
    msg = msg.replace(""""u'""", """"u'""")
    msg = msg.replace(", u'", ", '")
    msg = msg.replace(": u'", ": '")
    msg = msg.replace("{u'", "{'")
    msg = msg.replace("[u'", "['")
    msg = msg.replace("[{", "[{\n")
    msg = msg.replace("}]", "\n}]")
    msg = msg.replace(", '", ",\n'")
    msg = msg.replace(": {", ":\n{\n")
    msg = msg.replace("},", "\n},")
    for line in pformat(msg, indent=4, width=80, depth=2).split('\n'):
        line = line.replace("\\n", "")
        getattr(app.logger, level or "debug")(line)


def print_progress_bar(
        iteration,
        total,
        prefix='',
        suffix='',
        decimals=1,
        length=100,
        fill='#'):
    fill = '█'
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print()


def print_loading(msg, with_runtime=False):
    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            start = time.time()
            logger.info("Starting: {msg}".format(msg=msg.capitalize()))
            result = fn(*args, **kwargs)
            end = time.time()
            hours, rem = divmod(end - start, 3600)
            minutes, seconds = divmod(rem, 60)
            runtime = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
            logger.info("Runtime: {time} ({msg})".format(msg=msg, time="(" + str(runtime) + ")" if with_runtime else ""))
            # print(repr(fn), duration * 1000)
            return result
        return inner
    return decorator
