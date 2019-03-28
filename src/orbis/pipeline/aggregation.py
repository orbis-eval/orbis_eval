#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-




from orbis import app
from orbis.config import paths
from orbis.libs import aggregation_lib
from orbis.libs.files_lib import create_folder
import json

import os


class Aggregator(object):
    """The Aggregator class controls the aggregation of the data
    needed to evaluate the performance of the component beeing tested.

    The aggregator reads from the config what data is needed for the
    running test, what api is used to get the test data (the data to be
    compared to the gold standard, fetches the test data via the correct
    api and retrieves the gold standard data.

    All this data is then packed into a nice format to be further processed.

    Example::

        >>> a = aggregation.Aggregator.get_class(config)
        >>> data = a.run()


    """

    def __init__(self, yaml_config: dict) -> None:
        """
        Initializes all the values needed

        :param yaml_config: The configuration specified in the yaml file
        :type yaml_config: dict
        :raises ValueError: Error if no key named "aggregator" could be found.
        """

        # If no aggregator entries are available, the whole pipeline doesn't make sense
        # so we raise a Value Error and stop here.
        if not yaml_config.get("aggregator", False):
            raise ValueError("No aggregator specified in yaml file: {}".format(self.yaml_config["file_name"]))

        self.yaml_config = yaml_config
        self.data = {}

        # Fetching lenses, mappings and filters that where loaded when orbis started.
        self.lense = app.lenses
        self.mapping = app.mappings
        self.filter = app.filters

        self.service_name = self.yaml_config["aggregator"]["service"]["name"]
        self.location = self.yaml_config["aggregator"]["service"]["location"]
        self.file_name = self.yaml_config["file_name"]
        self.profile = self.yaml_config["aggregator"]["service"].get("profile", "None")

        self.data_set_name = self.yaml_config["aggregator"]["input"]["data_set"]["name"]
        self.data_set_path = os.path.join(paths.corpora_dir, self.data_set_name)
        self.computed_path = os.path.abspath(os.path.join(self.data_set_path, "computed", self.service_name))

        if self.yaml_config["aggregator"]["service"]["location"] == "local":
            self.computed_path = os.path.join(self.data_set_path, "computed", self.service_name)

        self.corpus_path = os.path.join(self.data_set_path, "corpus")
        self.gold_dir = os.path.join(self.data_set_path, "gold")

        self.cache_webservice = True if "cache_webservice_results" in self.yaml_config["savor"] else False

        self.config_dict = {
            "service_name": self.service_name,
            "location": self.location,
            "file_name": self.file_name,
            "profile": self.profile,
            "data_set_name": self.data_set_name,
            "data_set_path": self.data_set_path,
            "gold_dir": self.gold_dir,
            "computed_path": self.computed_path,
            "corpus_path": self.corpus_path,
            "data": self.data,
            "lense": self.lense,
            "mapping": self.mapping,
            "filter": self.filter,
            "plugin_name": self.service_name,
            "profile_name": self.profile,
            "save_output": True,
            "str_filter": self.filter
        }

    def load_data(self):

        # Getting corpus texts
        app.logger.info(f"Getting corpus texts for {self.yaml_config['file_name']}")
        self.data = aggregation_lib.get_corpus(self.config_dict, self.data)

        # Getting gold results
        app.logger.info(f"Getting Gold Results for {self.yaml_config['file_name']}")
        self.data = aggregation_lib.get_gold(self.config_dict, self.data)
        return self.data

    def run(self):
        """
        :return: Either the results from the webservice or the cached results.\
            depending on what is set in config["aggregator"]["service"]["location"]

        Example::

        >>> a = aggregation.Aggregator(config)
        >>> data = a.run()
        """

        self.data = self.load_data()
        # app.logger.debug(f">>> Data loaded: {self.data}")

        if self.location == "local":
            self.data = aggregation_lib.get_local(self.config_dict, self.data)

        if self.location == "web":
            self.data = aggregation_lib.get_from_webservice(self.config_dict, self.data)

        if self.cache_webservice:
            self.go_cache_webservice()

        # app.logger.debug(f"Data aggregated: {self.data}")
        return self.data

    def go_cache_webservice(self):
        data_set_name = self.yaml_config["aggregator"]["input"]["data_set"]["name"]
        data_set_path = os.path.join(paths.corpora_dir, data_set_name)
        service_name = self.yaml_config["aggregator"]["service"]["name"]
        path = os.path.join(data_set_path, "computed", service_name)

        create_folder(path)

        for number, item in self.data.items():
            with open(os.path.join(path, str(number) + ".json"), "w") as open_file:
                json.dump(item["computed"], open_file)
