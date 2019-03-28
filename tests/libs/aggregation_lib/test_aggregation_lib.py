#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


from orbis.libs import aggregation_lib
from orbis.libs import entity_preprocessing_lib
from pprint import pprint


text_0 = """The U.S. Patent Office allows genes to be patented as soon as someone isolates the DNA by removing it from the cell , says ACLU attorney Sandra Park ."""
text_1 = """Microsoft is an American multinational corporation \
    headquartered in Redmond, Washington, that develops, manufactures, \
    licenses, supports and sells computer software, consumer electronics \
    and personal computers and services. It was was founded by \
    Bill Gates and Paul Allen on April 4, 1975."""
text_2 = """In 1980, Steve dropped out of Stanford to join Microsoft, the company behind the Windows operating system."""

"""
def test_run_aida_api(text=None):
    result, runtime = aggregation_lib.run_aida_api(text=text)

    assert isinstance(result.json(), dict)


def test_get_from_aida():
    corpus_path = None
    lense = None
    mapping = None
    str_filter = None
    save_output = False
    config = {"file_name": "test.test"}
    data = None

    data = aggregation_lib.get_from_aida(
        corpus_path=corpus_path,
        data=data,
        lense=lense,
        mapping=mapping,
        str_filter=str_filter,
        save_output=save_output,
        config=config)

    assert data is not None


def test_run_babelnet_api(text=None):
    response, runtime = aggregation_lib.run_babelnet_api(text=text)
    assert response.json() is not None


def test_run_spotlight_api(text=None):
    response, runtime = aggregation_lib.run_spotlight_api(text=text)
    pprint(response)
    print("Runtime: {}".format(runtime))
    assert response.json() is not None

"""
