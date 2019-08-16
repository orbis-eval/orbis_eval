# -*- coding: utf-8 -*-

from logging.handlers import RotatingFileHandler
import logging
import os


def set_color(org_string, level=None):
    color_levels = {
        10: "\033[36m{}\033[0m",       # DEBUG
        20: "\033[32m{}\033[0m",       # INFO
        30: "\033[33m{}\033[0m",       # WARNING
        40: "\033[31m{}\033[0m",       # ERROR
        50: "\033[7;31;31m{}\033[0m"   # FATAL/CRITICAL/EXCEPTION
    }
    if level is None:
        return color_levels[20].format(org_string)
    else:
        return color_levels[int(level)].format(org_string)


def create_logger(app, maxBytes=False, backupCount=False):
    """ """

    maxBytes = maxBytes or 100000
    backupCount = backupCount or 1

    logger_format = app.settings.get('logger_format') or '%(levelname)-8s %(asctime)-25s %(module)-25s %(lineno)-5d %(message)s'
    level = app.settings['logging_level'] or 'debug'
    log_path = app.paths.log_path

    formatter = logging.Formatter(logger_format)
    logger = logging.getLogger()
    logger.setLevel(eval(f"logging.{level.upper()}"))

    """
    logger.info(set_color("test"))
    logger.debug(set_color("test", level=10))
    logger.warning(set_color("test", level=30))
    logger.error(set_color("test", level=40))
    logger.fatal(set_color("test", level=50))
    """

    error_log_path = os.path.join(log_path, "error.log")
    error_handler = RotatingFileHandler(error_log_path, maxBytes=maxBytes, backupCount=backupCount)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    info_log_path = os.path.join(log_path, "info.log")
    info_handler = RotatingFileHandler(info_log_path, maxBytes=maxBytes, backupCount=backupCount)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    debug_log_path = os.path.join(log_path, "debug.log")
    debug_handler = RotatingFileHandler(debug_log_path, maxBytes=maxBytes, backupCount=backupCount)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    logger.addHandler(debug_handler)

    warning_log_path = os.path.join(log_path, "warning.log")
    warning_handler = RotatingFileHandler(warning_log_path, maxBytes=maxBytes, backupCount=backupCount)
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)
    logger.addHandler(warning_handler)

    critical_log_path = os.path.join(log_path, "critical.log")
    critical_handler = RotatingFileHandler(critical_log_path, maxBytes=maxBytes, backupCount=backupCount)
    critical_handler.setLevel(logging.CRITICAL)
    critical_handler.setFormatter(formatter)
    logger.addHandler(critical_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(eval(f"logging.{level.upper()}"))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # print(console_handler.level)

    return logger


"""
import logging
import io

### Create the logger
logger = logging.getLogger('basic_logger')
logger.setLevel(logging.DEBUG)

### Setup the console handler with a StringIO object
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)

### Optionally add a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

### Add the console handler to the logger
logger.addHandler(ch)


### Send log messages.
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')


### Pull the contents back into a string and close the stream
log_contents = log_capture_string.getvalue()
log_capture_string.close()

### Output as lower case to prove it worked.
print(log_contents.lower())
"""
