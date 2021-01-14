# -*- coding: utf-8 -*-

"""Summary
"""

from datetime import datetime
from copy import deepcopy
import os
import uuid

from orbis_eval.core import app

import logging

logger = logging.getLogger(__name__)


class Rucksack(object):

    def __init__(self, config_file=None):
        """Summary

        Args:
            config_file (str): Description
        """
        super(Rucksack, self).__init__()

        if config_file:
            self.config = config_file
        else:
            self.config = None

        self.open = self.pack_rucksack()
        self.plugins = {}
        self.index = 0

    def pack_rucksack(self):

        rucksack = {}
        rucksack['config'] = deepcopy(self.config)
        rucksack['data'] = {}
        rucksack['data']['corpus'] = {}
        rucksack['data']['corpus_modified'] = {}
        rucksack['data']['gold'] = {}
        rucksack['data']['computed'] = {}
        rucksack['results'] = {}
        rucksack['data']['lense'] = app.lenses
        rucksack['data']['mapping'] = app.mappings
        rucksack['data']['filter'] = app.filters
        rucksack['data']['str_filter'] = app.filters
        rucksack['metadata'] = {'run': {}}
        rucksack['metadata']['run']['uuid'] = str(uuid.uuid4())
        rucksack['metadata']['corpus'] = {'source': None, 'download_time': None}

        if self.config:
            rucksack['config']['data_set_path'] = os.path.join(app.paths.corpora_dir,
                                                               self.config['aggregation']['input']['data_set']['name'])
            rucksack['config']['corpus_path'] = os.path.abspath(
                os.path.join(rucksack['config']['data_set_path'], 'corpus'))
            rucksack['config']['gold_path'] = os.path.abspath(os.path.join(rucksack['config']['data_set_path'], 'gold'))
            rucksack['config']['corpus_source_file'] = os.path.abspath(
                os.path.join(rucksack['config']['data_set_path'], 'source.txt'))
            if 'service' in self.config['aggregation']:
                rucksack['config']['computed_path'] = os.path.abspath(
                    os.path.join(rucksack['config']['data_set_path'], 'computed',
                                 self.config['aggregation']['service']['name'])) if \
                rucksack['config']['aggregation']['service']['location'] == "local" else None
            else:
                rucksack['config']['aggregation']['service'] = {'name': None, 'location': None}

            if 'evaluation' not in self.config:
                rucksack['config']['evaluation'] = {'name': None}
                rucksack['config']['scoring'] = {'name': None}
                rucksack['config']['metrics'] = {'name': None}

        return rucksack

    def load_plugin(self, name, plugin):

        self.plugins[name] = plugin

    def pack_gold(self, gold):

        self.open['data']['gold'] = gold

    def pack_source_and_downloadtime(self):

        with open(self.open['config']['corpus_source_file']) as open_file:
            content = open_file.read()
            # Downloaded from http://www.yovisto.com/labs/ner-benchmarks/data/dbpedia-spotlight-nif.ttl at 2020-05-18 14:50:23.625538
            source = content.split()[2]
            time = f'{content.split()[4]} {content.split()[5]}'
        self.open['metadata']['corpus']['source'] = source
        self.open['metadata']['corpus']['download_time'] = time

    def pack_corpus(self, corpus):
        # print(f"81: corpus: {corpus}")

        for doc, content in corpus.items():
            if doc.split("-")[-1] == "modified":
                self.open['data']['corpus_modified'][doc.replace("-modified", "")] = content
            else:
                self.open['data']['corpus'][doc] = content

        self.pack_source_and_downloadtime()

    def pack_computed(self, computed):

        self.open['data']['computed'] = computed

    def pack_results(self, results):

        raise NotImplemented

    def pack_results_summary(self, results_summary):

        raise NotImplemented

    def get_paths(self):

        raise NotImplemented

    """
    def natural_sort_key(self, keys):
        key_list = []
        max_len = max([len(str(key)) for key in keys])

        for key in [str(key) for key in keys]:
            if len(key) < max_len:
                diff = max_len - len(key)
                zeros = dif * "0"
                key = zeros + key
            key_list.append(key)
        key_list = sorted(key_list)

        key_list = [int()]


        key_list =
        print(max_len)
        return None

        return [int(text) if text.isdigit() else text.lower()
                for text in _nsre.split(keys)]
    """

    def get_keys(self):
        keys = []
        data = self.open['data']
        for key in data['corpus'].keys():
            keys.append(key)
        return keys

    def itemview(self, key):
        data = self.open['data']

        if data['corpus'].get(key, None):
            result = {
                'index': key,
                'corpus': data['corpus'].get(key, None),
                'corpus_modified': data['corpus_modified'].get(key, None),
                'gold': data['gold'].get(key, None),
                'computed': data['computed'].get(key, None)
            }
            return result
        else:
            return None

    def itemsview(self):
        data = self.open['data']
        for key, item in sorted(data['corpus'].items()):

            result = {
                'index': key,
                'url': data['gold'][key][0]['key'] if len(data['gold'][key]) else "",
                'corpus': item,
                'corpus_modified': data['corpus_modified'].get(key, None),
                'gold': data['gold'].get(key, None),
                'computed': data['computed'].get(key, None)
            }
            yield result

    def result_summary(self, specific=None):

        if "summary" in self.open['results']:
            summary = self.open['results']["summary"]
            results = summary.get(specific) if specific else summary
            return results
        return "No results calculated"

    def resultview(self, key, specific=None):
        if 'items' in self.open['results']:
            items = self.open['results']['items']
            if items.get(key):
                response = items[key]
                if specific:
                    response = response.get(specific)
                return response

        return {'confusion_matrix': {'fp_ids': [], 'tp_ids': [], 'fn_ids': []}}

    def resultsview(self, specific=None):
        items = self.open['results']['items']
        for key, results in sorted(items.items()):
            if specific:
                response = results.get(specific)
            else:
                response = {'index': key}
                for result_name, result in results.items():
                    response[result_name] = result
            yield response
