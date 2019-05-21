"""Summary
"""
import requests
import html
from urllib.parse import unquote_plus

from orbis import app
from orbis.plugins.aggregation import dbpedia_entity_types
from orbis.plugins.aggregation import monocle
from orbis.core.aggregation import AggregationBaseClass


class AidaAggregation(AggregationBaseClass):
    """docstring for AidaAggregation"""

    def __init__(self, rucksack):
        super(AidaAggregation, self).__init__()
        self.rucksack = rucksack
        self.file_name = self.rucksack.open['config']['file_name']
        self.lense = self.rucksack.open['data']['lense']
        self.mapping = self.rucksack.open['data']['mapping']
        self.str_filter = self.rucksack.open['data']['str_filter']

    def run(self):

        computed = {}
        for item in self.rucksack.itemsview():
            response = self.query(text=item['corpus'])
            if response:
                computed[item['index']] = self.file_entities(response)

        return computed

    def query(self, text=None):
        service_url = 'https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate'
        data = {'text': text}

        try:
            response = requests.post(service_url, data=data)
            response_json = response.json()
        except Exception as exception:
            app.logger.error("{}  ({})".format(exception, self.file_name))
            response_json = None

        return response_json

    def file_entities(self, response):

        file_entities = []

        for idx, item in enumerate(response["mentions"]):

            if len(item["allEntities"]) <= 0:
                continue

            identifier = item["bestEntity"]["kbIdentifier"]
            item["key"] = response["entityMetadata"][identifier]["url"]

            item["key"] = html.unescape(item["key"])
            item["key"] = unquote_plus(item["key"])
            item["key"] = item["key"].replace("\n", "")
            item["key"] = item["key"].replace("http://en.wikipedia.org/wiki/", "http://dbpedia.org/resource/")
            item["key"] = item["key"].replace(" ", "_")

            types = response["entityMetadata"][identifier]["type"]

            item["key"] = monocle.apply_mapping(self.mapping, item["key"])

            if 'YAGO_wordnet_person_100007846' in types:
                item["entity_type"] = 'Person'

            elif 'YAGO_yagoGeoEntity' in types:
                item["entity_type"] = 'Place'

            elif 'YAGO_wordnet_organization_108008335' in types:
                item["entity_type"] = 'Organization'

            else:
                item["entity_type"] = 'NoType'

            item["entity_type"] = dbpedia_entity_types.normalize_entity_type(item["entity_type"])
            item["document_start"] = int(item["offset"])
            item["document_end"] = int(item["document_start"] + int(item["length"]))
            item["surfaceForm"] = item["name"]

            in_lense = monocle.apply_lense(self.lense, item["key"])
            to_filter = monocle.apply_filter(self.str_filter, item["surfaceForm"])

            if in_lense or not to_filter:
                file_entities.append(item)

        return file_entities

    # def old_run(rucksack):

    #     computed = {}

    #     computed_path = rucksack.open['config']['computed_path']
    #     corpus_path = rucksack.open['config']['corpus_path']
    #     lense = rucksack.open['data']['lense']
    #     mapping = rucksack.open['data']['mapping']
    #     str_filter = rucksack.open['data']['str_filter']

    #     files = glob.glob(os.path.join(corpus_path, "*.txt"))
    #     sorted_files = sorted(files, key=lambda name: int(name.split("/")[-1].split(".")[0]))

    #     for file_dir in sorted_files:
    #         file_name = file_dir.split("/")[-1]
    #         file_number = file_name.split(".")[0]
    #         corpus_name = corpus_path.split("/data/")[-1].replace("/", "_")
    #         cached_file = os.path.abspath(os.path.join(computed_path, file_number + ".json"))

    #         if os.path.isfile(cached_file):
    #             app.logger.info("Already received from Aida: {}".format(file_dir.split("/")[-1]))
    #             continue

    #         app.logger.info("Querying Aida: {} ({})".format(file_name, corpus_name))

    #         with open(file_dir) as open_file:
    #             response = query(text=open_file.read())

    #         """
    #         try:
    #             response_json = response.json()
    #         except Exception as exception:
    #             app.logger.error("{}  ({})".format(exception, file_name))
    #         """

    #         computed[file_number]["computed"] = file_entities(response_json)
    #         app.logger.info("Received from Aida: {}".format(file_dir.split("/")[-1]))

    #     return run

