#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

'''
    .. moduleauthor:: Fabian Odoni fabian.odoni@htwchur.ch
'''

from orbis.lib import entity_preprocessing_lib


def test_build_source_path():
    for resource in ["filter", "mapping", "lense"]:
        filter_path = entity_preprocessing_lib.build_source_path("test", resource)
        path_fragments = filter_path.split("/")
        assert path_fragments[-1:-5:-1] == ['test.xz', f'{resource}s', 'data', 'orbis']


def test_load_lense():
    file_name = ["3.5-entity_list_en.txt-14dec-0130pm"]
    result = entity_preprocessing_lib.load_lense(file_names=file_name)

    assert isinstance(result, dict)


def test_load_mapping():
    file_name = ["redirects-v2.json-15dec-1121am"]
    result = entity_preprocessing_lib.load_mapping(file_names=file_name)

    assert isinstance(result, dict)


def test_load_filter():
    file_name = ["us_states_list_en-txt-12_jan_28-0913am"]
    result = entity_preprocessing_lib.load_filter(file_names=file_name)

    assert isinstance(result, dict)


"""
def test_convert_resources():
    source_path = entity_preprocessing_lib.build_source_path("test", resource)
    resource =

    entity_preprocessing_lib.convert_resources(source_path, resource)


def test_convert_mapping():
    source_path =
    resource =

    entity_preprocessing_lib.convert_mapping(source_path)


def test_convert_lense():
    source_path =
    resource =

    entity_preprocessing_lib.convert_lense(source_path)


def test_convert_filter():
    source_path =
    resource =

    entity_preprocessing_lib.convert_filter(source_path)
"""


if __name__ == '__main__':
    test_build_source_path()
