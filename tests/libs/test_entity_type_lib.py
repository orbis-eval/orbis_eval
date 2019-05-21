#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
    .. moduleauthor:: Fabian Odoni fabian.odoni@htwchur.ch
"""
import urllib
import regex

from orbis.lib.entity_type_lib import normalize_entity_type
from orbis.lib.entity_type_lib import get_dbpedia_type
from orbis.lib.entity_type_lib import get_sparql_redirect
from orbis.lib.entity_type_lib import get_regex_patterns
from orbis.config import regex_patterns


def test_regex():

    organization_pattern, person_pattern, location_pattern = get_regex_patterns()

    person_pattern = regex.compile(regex_patterns.base_pattern + "(" + "|".join(regex_patterns.person_pattern) + ")[0-9]*")
    result = person_pattern.match("http://schema.org/Person")

    assert result


def test_url_quoted():
    uri = "http://dbpedia.org/resource/Stephen_Hawking"
    uri_quoted = urllib.parse.quote(uri).encode("utf8")

    assert uri_quoted == b'http%3A//dbpedia.org/resource/Stephen_Hawking'


def test_get_sparql_redirect():
    endpoint_url = "http://dbpedia.org/sparql"

    uri = "http://dbpedia.org/resource/Steven_Hawking"

    result = get_sparql_redirect(endpoint_url, uri)
    assert result == 'http://dbpedia.org/resource/Steven_Hawking'


def test_normalize_entity_type():
    """ """

    assert normalize_entity_type("Random") == "Random"
    assert normalize_entity_type("random") == "Random"

    assert normalize_entity_type("location") == "Place"
    assert normalize_entity_type("Location") == "Place"

    assert normalize_entity_type("http://some.thing/location") == "Place"
    assert normalize_entity_type("http://some.thing/location/") == "Place"


def test_get_dbpedia_type():
    """ """
    uri = "http://dbpedia.org/resource/Stephen_Hawking"

    result = get_dbpedia_type(uri, check_redirect=True)
    assert result == "Person"


def main():
    test_regex()
    test_url_quoted()
    test_get_sparql_redirect()
    test_normalize_entity_type()
    test_get_dbpedia_type()


if __name__ == '__main__':
    main()
