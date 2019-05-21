"""Summary
"""
from copy import deepcopy
import os

from orbis import app


class Rucksack(object):

    """Summary

    Attributes:
        config (TYPE): Description
        index (int): Description
        open (TYPE): Description
        paths (object): Description
    """

    def __init__(self, config_file):
        """Summary

        Args:
            config_file (str): Description
        """
        super(Rucksack, self).__init__()

        self.config = config_file
        self.open = self.pack_rucksack()
        self.plugins = {}
        self.index = 0

    def pack_rucksack(self) -> dict:
        """Summary

        Returns:
            dict: Description
        """
        rucksack = {}

        rucksack['config'] = deepcopy(self.config)
        rucksack['data'] = {}
        rucksack['data']['corpus'] = {}
        rucksack['data']['gold'] = {}
        rucksack['data']['computed'] = {}
        rucksack['results'] = {}

        rucksack['data']['lense'] = app.lenses
        rucksack['data']['mapping'] = app.mappings
        rucksack['data']['filter'] = app.filters
        rucksack['data']['str_filter'] = app.filters
        rucksack['config']['data_set_path'] = os.path.join(app.paths.corpora_dir, self.config['aggregation']['input']['data_set']['name'])
        rucksack['config']['corpus_path'] = os.path.abspath(os.path.join(rucksack['config']['data_set_path'], 'corpus'))
        rucksack['config']['gold_path'] = os.path.abspath(os.path.join(rucksack['config']['data_set_path'], 'gold'))
        rucksack['config']['computed_path'] = os.path.abspath(os.path.join(rucksack['config']['data_set_path'], 'computed', self.config['aggregation']['service']['name'])) if rucksack['config']['aggregation']['service']['location'] == "local" else None

        return rucksack

    def load_plugin(self, name, plugin):
        self.plugins[name] = plugin

    def pack_gold(self, gold):
        """Summary

        Args:
            gold (TYPE): Description
        """
        self.open['data']['gold'] = gold

    def pack_corpus(self, corpus):
        """Summary

        Args:
            corpus (TYPE): Description
        """
        self.open['data']['corpus'] = corpus

    def pack_computed(self, computed):
        """Summary

        Args:
            computed (TYPE): Description
        """
        self.open['data']['computed'] = computed

    def pack_results(self, reults):
        """Summary

        Args:
            reults (TYPE): Description

        Raises:
            NotImplemented: Description
        """
        raise NotImplemented

    def pack_results_summary(self, results_summary):
        """Summary

        Args:
            results_summary (TYPE): Description

        Raises:
            NotImplemented: Description
        """
        raise NotImplemented

    def get_paths(self):
        """Summary

        Raises:
            NotImplemented: Description
        """
        raise NotImplemented

    def itemview(self, key):
        """Summary

        Yields:
            dict: Description
        """
        data = self.open['data']
        result = {
            'index': key,
            'corpus': data['corpus'].get(key, None),
            'gold': data['gold'].get(key, None),
            'computed': data['computed'].get(key, None)
        }
        return result

    def itemsview(self):
        """Summary

        Yields:
            dict: Description
        """
        data = self.open['data']

        for key, item in data['corpus'].items():
            result = {
                'index': key,
                'corpus': item,
                'gold': data['gold'].get(key, None),
                'computed': data['computed'].get(key, None)
            }
            yield result

    def result_summary(self, specific=None):
        """Summary

        Yields:
            dict: Description
        """
        summary = self.open['results']["summary"]
        results = summary.get(specific) if specific else summary
        return results

    def resultview(self, key, specific=None):

        items = self.open['results']['items']

        response = items[key]
        if specific:
            response = response.get(specific)
        return response

    def resultsview(self, specific=None):

        items = self.open['results']['items']

        for key, results in items.items():
            if specific:
                response = results.get(specific)
            else:
                response = {'index': key}
                for result_name, result in results.items():
                    response[result_name] = result

            yield response

    def check_config(self):
        """WIP

        Returns:
            TYPE: Description

        Raises:
            ValueError: Description
        """
        if not self.config.get('aggregation', False):
            raise ValueError(f"No aggregation specified in yaml file: {self.config['file_name']}")

        elif not self.config.get('aggregation', False):
            raise ValueError(f"No aggregation specified in yaml file: {self.config['file_name']}")

        elif not self.config.get('aggregation', False):
            raise ValueError(f"No aggregation specified in yaml file: {self.config['file_name']}")

        elif not self.config.get('aggregation', False):
            raise ValueError(f"No aggregation specified in yaml file: {self.config['file_name']}")

        else:
            return True

    """
    def __iter__(self):

        return self

    def __next__(self):

        try:
            item = self.__getitem__(self.index)
            self.index += 1
        except IndexError:
            raise StopIteration

        return result

    def __getitem__(self, index):  #aka itemview
        try:
            corpus = self.open['data']['corpus'][self.index]
        except IndexError:
            raise IndexError

        result = {
            'index': self.index,
            'corpus': corpus,
            'gold': self.open['data']['gold'].get(self.index, None),
            'computed': self.open['data']['computed'].get(self.index, None)
        }

        self.index += 1

        return result
    """
