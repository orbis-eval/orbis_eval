# -*- coding: utf-8 -*-

import os
from datetime import datetime

from orbis_eval import app
from orbis_eval.libs import orbis_setup

import logging
logger = logging.getLogger(__name__)

try:
    from orbis_plugin_aggregation_monocle import Main as monocle
except ModuleNotFoundError:
    logger.warning("Monocle not found. Please install to use. 'pip install --upgrade orbis-plugin-aggregation-monocle'")


class PluginBaseClass(object):
    """docstring for PluginBaseClass"""

    def __init__(self):
        super(PluginBaseClass, self).__init__()

    def get_plugin_dir(self, file):
        plugin_dir = os.path.abspath("/".join(os.path.realpath(file).split("/")[:-2]))
        return plugin_dir

    def catch_data(self, variable, function_name, file_name, file):
        plugin_dir = self.get_plugin_dir(file)
        data_dir = plugin_dir + "/tests/data/"
        with open(data_dir + function_name + "_" + file_name, "w") as open_file:
            open_file.write(str(variable))


class AggregationBaseClass(PluginBaseClass):

    def __init__(self, rucksack):
        super(AggregationBaseClass, self).__init__()
        self.app = app
        self.rucksack = rucksack
        self.config = self.rucksack.open['config']
        self.data = self.rucksack.open['data']
        self.results = self.rucksack.open['results']
        self.file_name = self.config['file_name']
        self.lense = self.data['lense']
        self.mapping = self.data['mapping']
        self.str_filter = self.data['str_filter']
        self.environment_variables = self.get_environment_variables()

    def environment(self):
        return {}

    def get_environment_variables(self):
        keys = self.environment()
        variables = {}

        for key, value in keys.items():
            try:
                variables[key] = os.environ[key]
            except KeyError:
                logger.error(f"Environment variable {key} not found.")
                """
                logger.error(f"Environment variable {key} not found. Please enter manually.")
                # Doesnt work with multiprocessing
                # https://stackoverflow.com/questions/7489967/python-using-stdin-in-child-process/15766145#15766145
                manual_value = input()
                logger.error(f"Manual value: {manual_value}")
                os.environ[key] = manual_value
                variables[key] = manual_value
                """
                variables[key] = None
        return variables

    def run(self):
        computed = {}
        for item in self.rucksack.itemsview():
            start = datetime.now()
            response = self.query(item)
            duration = datetime.now() - start
            if response:
                logger.info(f"Queried Item {self.file_name}: {item['index']} ({duration})")
                computed[item['index']] = self.get_computed(response, item)
            else:
                logger.info(f"Queried Item {self.file_name}: {item['index']} ({duration}) - Failed")
                computed[item['index']] = []
        return computed

    def get_computed(self, response, item):
        if not response:
            return None

        data = {
            "lense": self.lense,
            "mapping": self.mapping,
            "str_filter": self.str_filter
        }

        entities = self.map_entities(response, item)

        # entities = monocle.run_monocle(entities, data)
        try:
            entities = monocle.run_monocle(entities, data)
        except NameError as exception:
            logger.warning(f"Monocle not installed. Nothing done. {exception}")

        return entities

    def query(self, item):

        return NotImplementedError

    def map_entities(self, response, item):

        return NotImplementedError

    def _run_monocle(self, entities):
        result = []

        for item in entities:
            item["key"] = monocle.apply_mapping(self.mapping, item["key"])
            in_lense = monocle.apply_lense(self.lense, item["key"])
            to_filter = monocle.apply_filter(self.str_filter, item["surfaceForm"])

            if in_lense or not to_filter:
                result.append(item)

        return result


class AddonBaseClass(object):
    """docstring for AddonBaseClass"""

    def __init__(self):
        super(AddonBaseClass, self).__init__()
        self.addon_path = None
        self.metadata = self.load_metadata()

    def get_description(self):
        init_path = os.path.join(self.addon_path, '__init__.py')
        self.description = orbis_setup.load_metadata(init_path)['description']
