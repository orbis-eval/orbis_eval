#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import pkgutil
from orbis_eval import app
import os

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms import SelectMultipleField

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
        if name.startswith(f'orbis_plugin_{stage}')
        and name not in blacklist
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


class ConfigForm(FlaskForm):

    aggregation__service__name = SelectField(
        label='Aggregation',
        choices=get_modules('aggregation')
    )

    aggregation__service__location = SelectField(
        label='Location',
        choices=[('web', 'web'), ('local', 'local')]
    )

    aggregation__input__data_set__name = SelectField(
        label='Corpus',
        choices=get_corpora()
    )

    evaluation__name = SelectField(
        label='Evaluation',
        choices=get_modules('evaluation')
    )

    scoring__name = SelectField(
        label='Scoring',
        choices=get_modules('scoring')
    )

    scoring__condition = StringField()
    scoring__ignore_empty = StringField()

    metrics__name = SelectField(
        label='Metrics',
        choices=get_modules('metrics')
    )

    storage__name = SelectMultipleField(
        label='Storage',
        choices=get_modules('storage')
    )


if __name__ == '__main__':
    print(get_modules('aggregation'))
    # print(get_modules('evaluation'))
    # print(get_modules('scoring'))
    # print(get_modules('metrics'))
    # print(get_modules('storage'))
    # print(get_corpora())

"""

aggregation:
  service:
    name: aida
    location: local
  input:
    data_set:
      name: rss1

evaluation:
  name: binary_classification_evaluation

scoring:
  name: nel_scorer
  condition: overlap
  ignore_empty: False

metrics:
  name: binary_classification_metrics

storage:
  - csv_result_list
  - html_pages

"""
