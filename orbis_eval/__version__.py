__name__ = "orbis_eval"
__version__ = "2.2.4"
__author__ = "fabod"
__year__ = "2019"
__description__ = "An Extendable Evaluation Pipeline for Named Entity Drill-Down Analysis"
__license__ = "GPL2"
__min_python_version__ = "3.6"
__requirements_file__ = "requirements.txt"
__url__ = "https://orbis-eval.github.io/Orbis/"
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
    "orbis_plugin_aggregation_dbpedia_entity_types",
    "orbis_plugin_aggregation_monocle",
    "orbis_plugin_aggregation_gold_gs",
    "orbis_plugin_aggregation_serial_corpus",
    "orbis_plugin_aggregation_local_cache",
    "orbis_plugin_aggregation_aida",
    "orbis_plugin_aggregation_babelfly",
    "orbis_plugin_aggregation_spotlight",
    "orbis_plugin_evaluation_binary_classification_evaluation",
    "orbis_plugin_metrics_binary_classification_metrics",
    "orbis_plugin_scoring_nel_scorer",
    "orbis_plugin_storage_cache_webservice_results",
    "orbis_plugin_storage_csv_result_list",
    "orbis_plugin_storage_html_pages"
]
__addons__ = [
    "orbis_addon_repoman"
]
