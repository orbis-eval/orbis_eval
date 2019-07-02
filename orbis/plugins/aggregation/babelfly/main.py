import os
import requests

from orbis import app
from orbis.plugins.aggregation import dbpedia_entity_types
from orbis.core.aggregation import AggregationBaseClass


class BabelflyAggregator(AggregationBaseClass):

    def query(self, text, item):
        service_url = 'https://babelfy.io/v1/disambiguate'
        key = os.environ['BABELNET_API_KEY']
        annotation_type = 'NAMED_ENTITIES'
        data = {
            'text': text,
            'annType': annotation_type,
            'key': key
        }
        try:
            response = requests.post(service_url, data=data).json()
        except Exception as exception:
            app.looger.error(f"Query failed: {exception}")
            response = None
        return response

    def map_entities(self, response, item):
        if not response:
            return None
        corpus = item['corpus']
        file_entities = []
        for item in response:
            item["key"] = item["DBpediaURL"]
            item["entity_type"] = dbpedia_entity_types.get_dbpedia_type(item["key"])
            item["entity_type"] = dbpedia_entity_types.normalize_entity_type(item["entity_type"])
            item["document_start"] = int(item["charFragment"]["start"])
            item["document_end"] = int(item["charFragment"]["end"] + 1)
            item["surfaceForm"] = corpus[item["document_start"]:item["document_end"]]
            file_entities.append(item)
        return file_entities
