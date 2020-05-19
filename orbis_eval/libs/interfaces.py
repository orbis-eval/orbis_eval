#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pkgutil
from orbis_eval.core import app
import os

blacklist = {
    'orbis_plugin_aggregation_local_cache',
    'orbis_plugin_aggregation_monocle',
    'orbis_plugin_aggregation_gold_gs',
    'orbis_plugin_aggregation_dbpedia_entity_types',
    'orbis_plugin_aggregation_serial_corpus'
}


def get_modules(stage):
    plugins = [
        # (' '.join(name.split('_')[3:]), name)
        (name, name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith(f'orbis_plugin_{stage}') and name not in blacklist
    ]
    return plugins


def get_corpora():
    corpora_dir = app.paths.corpora_dir
    corpora = [
        (dirnames, dirnames)
        for dirnames
        in os.listdir(corpora_dir)
        if os.path.isdir(os.path.join(corpora_dir, dirnames))
    ]
    return corpora
