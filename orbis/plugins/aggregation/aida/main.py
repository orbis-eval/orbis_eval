"""Summary
"""
import requests
import html
from urllib.parse import unquote_plus

from orbis import app
from orbis.plugins.aggregation import dbpedia_entity_types
from orbis.core.aggregation import AggregationBaseClass


class AidaAggregator(AggregationBaseClass):
    """docstring for AidaAggregator"""

    def query(self, text, item):
        service_url = 'https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate'
        data = {'text': item['corpus']}
        try:
            response = requests.post(service_url, data=data).json()
        except Exception as exception:
            app.looger.error(f"Query failed: {exception}")
            response = None
        return response

    def map_entities(self, response, item):

        file_entities = []
        for item in response["mentions"]:
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

            file_entities.append(item)

        return file_entities
