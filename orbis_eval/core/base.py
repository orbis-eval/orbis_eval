# -*- coding: utf-8 -*-
"""Summary

Attributes:
    logger (TYPE): Description
"""

import os
from datetime import datetime

from orbis_eval.core import app
from orbis_eval.libs import orbis_setup

import logging
logger = logging.getLogger(__name__)

try:
    from orbis_eval.plugins.aggregation.monocle import Main as monocle
except ModuleNotFoundError:
    logger.warning("Monocle not found. Please install to use. 'pip install --upgrade orbis-plugin-aggregation-monocle'")


class PluginBaseClass(object):
    """ Provides some basic methods for all Plugins. Shoudl not be used
    directly. Use on of the specific plugin classes that are based on this
    class. (Use its children...)
    """

    def __init__(self):
        """Summary
        """
        super(PluginBaseClass, self).__init__()

    def get_plugin_dir(self, file):
        """Get the path of a path and returns the directory of that file.
        Usually used to get the directory where the plugin is located.

        Args:
            file (str): A file path as string.

        Returns:
            TYPE: A directory path containing the file of the provided file path.
        """
        plugin_dir = os.path.abspath("/".join(os.path.realpath(file).split("/")[:-2]))
        return plugin_dir

    def catch_data(self, variable, function_name, file_name, file):
        """WIP: Should catch data and save it. To use this method, call it from within
        the plugin that is based on a Plugin base class

        Args:
            variable (TYPE): Description
            function_name (TYPE): Description
            file_name (TYPE): Description
            file (TYPE): Description
        """
        if app.settings["catch_data"]:
            plugin_dir = self.get_plugin_dir(file)
            data_dir = plugin_dir + "/tests/data/"

            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            with open(data_dir + function_name + "_" + file_name, "w") as open_file:
                open_file.write(str(variable))


class AggregationBaseClass(PluginBaseClass):

    """Summary
    """

    def __init__(self, rucksack):
        """Summary

        Args:
            rucksack (TYPE): Description
        """
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
        """Summary

        Returns:
            TYPE: Description
        """
        return {}

    def get_environment_variables(self):
        """Summary

        Returns:
            TYPE: Description
        """
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
        """Summary

        Returns:
            TYPE: Description
        """
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
        """Summary

        Args:
            response (TYPE): Description
            item (TYPE): Description

        Returns:
            TYPE: Description
        """
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
        """Summary

        Args:
            item (TYPE): Description

        Returns:
            TYPE: Description
        """
        return NotImplementedError

    def map_entities(self, response, item):
        """Summary

        Args:
            response (TYPE): Description
            item (TYPE): Description

        Returns:
            TYPE: Description
        """
        return NotImplementedError

    def _run_monocle(self, entities):
        """Summary

        Args:
            entities (TYPE): Description

        Returns:
            TYPE: Description
        """
        result = []

        for item in entities:
            item["key"] = monocle.apply_mapping(self.mapping, item["key"])
            in_lense = monocle.apply_lense(self.lense, item["key"])
            to_filter = monocle.apply_filter(self.str_filter, item["surfaceForm"])

            if in_lense or not to_filter:
                result.append(item)

        return result


class AddonBaseClass(object):
    """docstring for AddonBaseClass

    Attributes:
        addon_path (TYPE): Description
        description (TYPE): Description
        metadata (TYPE): Description
    """

    def __init__(self):
        """Summary
        """
        super(AddonBaseClass, self).__init__()
        self.addon_path = None
        self.metadata = self.load_metadata()

    def get_description(self):
        """Summary
        """
        init_path = os.path.join(self.addon_path, '__init__.py')
        self.description = orbis_setup.load_metadata(init_path)['description']
