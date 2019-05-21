import spotlight

from orbis import app
from orbis.plugins.aggregation import dbpedia_entity_types
from orbis.core.aggregation import AggregationBaseClass


class SpotlightAggregator(AggregationBaseClass):
    """docstring for SpotlightAggregator"""

    def query(self, text, item):
        client = 'http://model.dbpedia-spotlight.org/de/annotate'
        only_pol_filter = {
            'policy': 'whitelist',
            'types': 'DBpedia:Person, DBpedia:Place, DBpedia:Location, DBpedia:Organisation, Http://xmlns.com/foaf/0.1/Person',
            'coreferenceResolution': True
        }
        try:
            response = spotlight.annotate(client, text=text, filters=only_pol_filter)
        except Exception as exception:
            app.looger.error(f"Query failed: {exception}")
            response = None
        return response

    def map_entities(self, response, item):
        entities = []

        for idx, item in enumerate(response):

            item["key"] = item["URI"]
            item["key"] = item["key"].replace("http://en.wikipedia.org/wiki/", "http://dbpedia.org/resource/")
            item["key"] = item["key"].replace("http://de.dbpedia.org/resource/", "http://dbpedia.org/resource/")

            item = self.get_type(item)
            item["document_start"] = int(item["offset"])
            item["document_end"] = int(item["offset"]) + len(item["surfaceForm"])
            entities.append(item)

        return entities

    def get_type(self, item):
        places = ["place", "location", "settlement"]
        persons = ['http://xmlns.com/foaf/0.1/person', 'person']
        orgs = ["organisation"]
        item["entity_type"] = "NoType"

        for place in places:
            if place in item["types"].lower():
                item["entity_type"] = dbpedia_entity_types.normalize_entity_type("location")
        for person in persons:
            if person in item["types"].lower():
                item["entity_type"] = dbpedia_entity_types.normalize_entity_type("person")
        for org in orgs:
            if org in item["types"].lower():
                item["entity_type"] = dbpedia_entity_types.normalize_entity_type("organisation")

        return item
