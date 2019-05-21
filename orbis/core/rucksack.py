from copy import deepcopy
import os

from orbis import app


class Rucksack(object):

    def __init__(self, config_file):
        super(Rucksack, self).__init__()
        self.config = config_file
        self.open = self.pack_rucksack()
        self.plugins = {}
        self.index = 0

    def pack_rucksack(self) -> dict:
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
        self.open['data']['gold'] = gold

    def pack_corpus(self, corpus):
        self.open['data']['corpus'] = corpus

    def pack_computed(self, computed):
        self.open['data']['computed'] = computed

    def pack_results(self, reults):
        raise NotImplemented

    def pack_results_summary(self, results_summary):
        raise NotImplemented

    def get_paths(self):
        raise NotImplemented

    def itemview(self, key):
        data = self.open['data']
        result = {
            'index': key,
            'corpus': data['corpus'].get(key, None),
            'gold': data['gold'].get(key, None),
            'computed': data['computed'].get(key, None)
        }
        return result

    def itemsview(self):
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
