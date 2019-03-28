#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from orbis import app
from orbis.libs import savor_lib

import datetime


class Savor(object):
    """

    """

    def __init__(self, config, data, results):

        self.config = config
        self.data = data
        self.results = results
        self.date = "{:%Y-%m-%d_%H:%M:%S.%f}".format(datetime.datetime.now())

    def run(self):

        # app.logger.debug(self.config["savor"])
        for item in self.config["savor"]:
            app.logger.debug(f"Running: {item}")

            plugin_module = savor_lib.get_plugin(item)
            plugin_module.run(self.config, self.data, self.results)
