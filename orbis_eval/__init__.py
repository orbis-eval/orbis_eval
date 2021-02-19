# -*- coding: utf-8 -*-
__name__ = "orbis_eval"
__version__ = "2.3.1"
__author__ = "fabod, rogerwaldvogel"
__year__ = "2021"
__description__ = "An Extendable Evaluation Pipeline for Named Entity Drill-Down Analysis"
__license__ = "GPL2"
__min_python_version__ = "3.6"
__requirements_file__ = "requirements.txt"
__url__ = "https://github.com/orbis-eval/orbis_eval"
__type__ = "main"
__classifiers__ = [
    "Framework :: orbis-eval",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3.7"
]
__plugins__ = [
    "orbis_plugin_aggregation_local_cache",
    "orbis_plugin_aggregation_aida",
    "orbis_plugin_aggregation_babelfly",
    "orbis_plugin_aggregation_spotlight",
    "orbis_plugin_evaluation_binary_classification_evaluation",
    "orbis_plugin_metrics_binary_classification_metrics",
    "orbis_plugin_scoring_nel_scorer",
    "orbis_plugin_scoring_ner_scorer",
    "orbis_plugin_storage_cache_webservice_results",
    "orbis_plugin_storage_csv_result_list",
    "orbis_plugin_storage_html_pages"
]
__addons__ = [
    "orbis_addon_repoman"
]
