# -*- coding: utf-8 -*-

import os

from orbis_eval import app
from orbis_eval.libs import orbis_setup
from orbis_plugin_aggregation_monocle import Main as monocle


class AggregationBaseClass(object):

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

    def run(self):
        computed = {}
        for item in self.rucksack.itemsview():
            response = self.query(item)
            if response:
                computed[item['index']] = self.get_computed(response, item)
        return computed

    def get_computed(self, response, item):
        if not response:
            return None

        entities = self.map_entities(response, item)
        entities = self.run_monocle(entities)

        return entities

    def query(self, item):

        return NotImplementedError

    def map_entities(self, response, item):

        return NotImplementedError

    def run_monocle(self, entities):
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
