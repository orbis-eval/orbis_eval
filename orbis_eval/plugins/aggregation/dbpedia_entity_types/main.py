# -*- coding: utf-8 -*-

import re
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLExceptions

import orbis_eval.plugins.aggregation.dbpedia_entity_types.regex_patterns as regex_patterns

import logging
logger = logging.getLogger(__name__)


class Main(object):
    """docstring for Main"""

    def __init__(self):
        super(Main, self).__init__()

    @classmethod
    def normalize_entity_type(cls, entity_type: str) -> str:
        mapping = {
            "location": "place",
            "organisation": "organization",
            "notype": "undefined",
            "notfound": "undefined"
            }

        entity_type = entity_type.strip("/").split("/")[-1]
        mapped_entity_type = mapping.get(entity_type.lower(), None)
        if mapped_entity_type:
            entity_type = mapped_entity_type.capitalize()
        return entity_type

    @classmethod
    def get_sparql_redirect(cls, endpoint_url, uri):
        redirect_query = f"""
            SELECT DISTINCT ?redirected
            WHERE
            {{
                <{uri}> <http://dbpedia.org/ontology/wikiPageRedirects> ?redirected .
            }}
        """
        try:
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(redirect_query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            redirect_uri = results["results"]["bindings"][0]["redirected"]["value"]
        except Exception:
            redirect_uri = uri
        if redirect_uri == uri:
            redirect_uri = uri
        return uri

    @classmethod
    def get_dbpedia_type(cls, uri, check_redirect=False):
        endpoint_url = "http://dbpedia.org/sparql"
        if check_redirect:
            uri = cls.get_sparql_redirect(endpoint_url, uri)
        # uri = urllib.parse.quote(uri).encode("utf8")
        query: str = (
            f'\nSELECT DISTINCT ?obj'
            f'\nWHERE'
            f'\n{{'
            f'\n  <{uri}> (rdf:type)* ?obj .'
            f'\n}}'
        )
        # logger.debug(f"sparql-query:\n{query}\n")

        try:
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            if len(results["results"]["bindings"]) <= 0:
                entity_type = "undefined"
            else:
                results = [result["obj"]["value"] for result in results["results"]["bindings"]]
                entity_type = cls.categorize_types(results)
        except SPARQLExceptions.QueryBadFormed:
            logger.debug(f"erroneous sparql-query:\n{query}\n")
            entity_type = "undefined"

        return entity_type

    @classmethod
    def get_regex_patterns(cls, ):
        base_pattern = regex_patterns.base_pattern
        organization_pattern = re.compile(base_pattern + "(" + "|".join(
            regex_patterns.organization_pattern) + ")[0-9]*")
        person_pattern = re.compile(base_pattern + "(" + "|".join(regex_patterns.person_pattern) + ")[0-9]*")
        location_pattern = re.compile(base_pattern + "(" + "|".join(regex_patterns.location_pattern) + ")[0-9]*")
        return organization_pattern, person_pattern, location_pattern

    @classmethod
    def get_first_best_entity_type(cls, results, not_found_uris=None):
        organization_pattern, person_pattern, location_pattern = cls.get_regex_patterns()
        for result in results:
            result = str(result)
            if organization_pattern.match(result):
                entity_type = 'Organisation'
                break
            elif person_pattern.match(result):
                entity_type = 'Person'
                break
            elif location_pattern.match(result):
                entity_type = 'Location'
                break
            elif "http://aksw.org/notInWiki" in result:
                entity_type = 'notInWiki'
                break
            else:
                entity_type = False
                if not_found_uris:
                    not_found_uris.append(result)
        return entity_type

    @classmethod
    def get_most_mentioned_entity_type(cls, results, not_found_uris=None):
        entity_types = {
            'Organisation': 0,
            'Person': 0,
            'Location': 0,
            'notInWiki': 0,
            'notFound': 0
        }
        organization_pattern, person_pattern, location_pattern = cls.get_regex_patterns()
        for result in results:
            result = str(result)
            if organization_pattern.match(result):
                entity_types['Organisation'] += 1
            elif person_pattern.match(result):
                entity_types['Person'] += 1
            elif location_pattern.match(result):
                entity_types['Location'] += 1
            elif "http://aksw.org/notInWiki" in result:
                entity_types['notInWiki'] += 1
            else:
                if not_found_uris:
                    not_found_uris.append(result)

        logger.debug(f"Entity type pattern matching results: {entity_types}")
        max_entity_type = ('notFound', 1)
        for entity_type, count in entity_types.items():
            if count >= max_entity_type[1]:
                max_entity_type = (entity_type, count)
        return max_entity_type[0]

    @classmethod
    def categorize_types(cls, results):
        organization_pattern, person_pattern, location_pattern = cls.get_regex_patterns()
        not_found_uris = []
        # can be multiple types, must build a check
        entity_type = cls.get_most_mentioned_entity_type(results, not_found_uris=None)
        # entity_type = cls.get_first_best_entity_type(results, not_found_uris=None)
        if not entity_type or entity_type == 'notInWiki':
            logger.warning(f"[dbpedia-entity-types] No entity type found")
            entity_type = "undefined"
        else:
            logger.debug(f"Entity type found: {entity_type}")
        return entity_type

    """
    @classmethod
    def normalize_tags(cls, input_entity, evaluator):
        if app.settings.entity_maps.get(evaluator):
            entity_mappings = app.settings.entity_maps[evaluator]
            for entity, replacement in entity_mappings.items():
                if entity == input_entity:
                    return replacement
        return input_entity
    """
