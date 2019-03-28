#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import os
import logging
from logging.handlers import RotatingFileHandler

from orbis.config import paths
from orbis.config import settings


def create_logger(maxBytes=False, backupCount=False):
    """ """

    maxBytes = maxBytes or 100000
    backupCount = backupCount or 1

    logger_format = settings.logger_format
    logging_level = settings.logging_level
    log_path = paths.log_path

    formatter = logging.Formatter(logger_format)
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

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
    console_handler.setLevel(eval(f"logging.{logging_level.upper()}"))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

"""
    LOG_CONFIG = {
        'version':1,
        'formatters':{
            'error':{'format':ERROR_FORMAT},
            'debug':{'format':DEBUG_FORMAT}},
            'handlers':{
                'console':{
                    'class':'logging.StreamHandler',
                    'formatter':'debug',
                    'level':logging.DEBUG},
                'file':{
                    'class':'logging.FileHandler',
                     'filename':'/usr/local/logs/DatabaseUpdate.log',
                     'formatter':'error',
                     'level':logging.ERROR}},
          'root':{
            'handlers':('console', 'file')}
    }

    handlers:
      console:
        class : logging.StreamHandler
        formatter: brief
        level   : INFO
        filters: [allow_foo]
        stream  : ext://sys.stdout
      file:
        class : logging.handlers.RotatingFileHandler
        formatter: precise
        filename: logconfig.log
        maxBytes: 1024
        backupCount: 3

    logging.config.dictConfig(LOG_CONFIG)
"""
