import glob
import os
import urllib

from orbis_eval.plugins.aggregation.dbpedia_entity_types import Main as dbpedia_entity_types
from orbis_eval.plugins.aggregation.monocle import Main as monocle

from .gold_file_handler import GoldFileHandler

import logging

logger = logging.getLogger(__name__)


class GsHandler(GoldFileHandler):
    def __init__(self, rucksack, gold_path):
        super().__init__(rucksack, gold_path)

    def run(self):
        gold_standard = {}
        for file_dir in self.get_files(self.gold_path):
            gold_standard = self.extract_gold(
                file_dir,
                self.corpus,
                self.mapping,
                self.lense,
                self.filter
            )
        return gold_standard

    @staticmethod
    def get_files(gold_path):
        for file_dir in glob.glob(os.path.abspath(os.path.join(gold_path, '*.gs'))):
            yield file_dir

    def map_items(self, line, corpus, mapping, lense, filter):
        # gs file structure:
        # ---------------------
        #  0    1    2   3    4    5        6
        # doc|start|end|url|score|type|surface_form

        nuggets = line.strip().split("\t")
        file_number = nuggets[0]
        start = int(nuggets[1])
        end = int(nuggets[2])
        url = urllib.parse.unquote(nuggets[3])
        score = nuggets[4]
        type_url = nuggets[5]

        try:
            surface_form = nuggets[6]
        except:
            print("No surface form in gold")
            surface_form = corpus[file_number][start:end]
        # logger.debug(f"Processing: {url}: {surface_form} ({type_url})")
        url = monocle.apply_mapping(mapping, url)
        in_lense = monocle.apply_lense(lense, url)
        to_filter = monocle.apply_filter(filter, surface_form)

        entity_type = dbpedia_entity_types.normalize_entity_type(type_url.split("/")[-1])

        return file_number, start, end, url, score, type_url, surface_form, in_lense, to_filter, entity_type

    def extract_gold(self, file_dir, corpus, mapping, lense, filter):
        gold = {}

        with open(file_dir) as open_file:
            for line in open_file.readlines():

                # gs file structuring:
                # ---------------------
                #  0    1    2   3    4    5        6
                # doc|start|end|url|score|type|surface_form

                file_number, start, end, url, score, \
                type_url, surface_form, in_lense, to_filter, \
                entity_type = self.map_items(line, corpus, mapping, lense, filter)

                if in_lense and not to_filter:
                    logger.debug(f"Adding {surface_form}")
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
                    # logger.debug(f"Not adding to gold: {surface_form}")
                    pass
                # logger.debug(f"gefile_numbert_gold: {gold[file_number]}")
        return gold
