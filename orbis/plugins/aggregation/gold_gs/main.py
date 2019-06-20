import glob
import os
import urllib

from orbis import app
from orbis.plugins.aggregation import dbpedia_entity_types
from orbis.plugins.aggregation import monocle


class GoldGS(object):

    def __init__(self, rucksack, path=None):
        super(GoldGS, self).__init__()
        self.rucksack = rucksack

        if not path:
            self.gold_path = self.rucksack.open['config']['gold_path']
        else:
            self.gold_path = path

        self.lense = self.rucksack.open['data']['lense']
        self.mapping = self.rucksack.open['data']['mapping']
        self.filter_ = self.rucksack.open['data']['filter']
        self.corpus = self.rucksack.open['data']['corpus']

    def run(self):
        gold = {}
        for file_dir in glob.glob(os.path.abspath(os.path.join(self.gold_path, '*.gs'))):
            print(f">>>>> FILE DIR: {file_dir}")

            with open(file_dir) as open_file:
                for line in open_file.readlines():

                    # gs file structuring:
                    # ---------------------
                    #  0    1    2   3    4    5
                    # doc|start|end|url|score|type|

                    nuggets = line.split()
                    file_number = nuggets[0]
                    start = int(nuggets[1])
                    end = int(nuggets[2])
                    url = urllib.parse.unquote(nuggets[3])
                    score = nuggets[4]
                    type_url = nuggets[5]
                    surface_form = self.corpus[file_number][start:end]
                    # app.logger.debug(f"Processing: {url}: {surface_form} ({type_url})")
                    url = monocle.apply_mapping(self.mapping, url)
                    in_lense = monocle.apply_lense(self.lense, url)
                    to_filter = monocle.apply_filter(self.filter_, surface_form)
                    entity_type = dbpedia_entity_types.normalize_entity_type(type_url.split("/")[-1])
                    if in_lense and not to_filter:
                        app.logger.debug(f"Adding {surface_form}")
                        gold[file_number] = gold.get(file_number, [])
                        gold[file_number].append({
                            'id': file_number,
                            'start': start,
                            'end': end,
                            'key': url,
                            'score': score,
                            'entity_type': entity_type,
                            'type_url': type_url,
                            'surfaceForm': surface_form
                        })
                    else:
                        # app.logger.debug(f"Not adding to gold: {surface_form}")
                        pass
                    # app.logger.debug(f"gefile_numbert_gold: {gold[file_number]}")
        return gold
