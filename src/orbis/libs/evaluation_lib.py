#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-



from orbis import app
from orbis.libs import scorer_lib
from orbis.libs import metrics_lib

import importlib


def get_evaluation(config):
    """

    :param config:
    :raises: ValueError
    :return:
    """

    try:
        plugin_name = config["plugin_name"]

    except Exception:
        error = ValueError("plugin_name not found in config.")
        app.logger.critical(error)
        raise ValueError(error)

    evaluation = importlib.import_module("orbis.plugins.evaluators.{plugin_name}.{plugin_name}".format(plugin_name=plugin_name))

    return evaluation.run(config)


def get_conditions(config):
        if config["scorer"]["name"] == "NEL_ScorerSimple":
            conditions = ["same_url", "same_type", "same_surfaceForm"]
            app.logger.info("Running NEL_ScorerSimple for {}".format(config["file_name"]))

        elif config["scorer"]["name"] == "NEL_ScorerStrict":
            conditions = ["same_start", "same_end", "same_url", "same_type", "same_surfaceForm"]
            app.logger.info("Running NEL_ScorerStrict for {}".format(config["file_name"]))

        elif config["scorer"]["name"] == "NEL_ScorerOverlap":
            conditions = ["overlap", "same_url", "same_type"]
            app.logger.info("Running NEL_ScorerOverlap for {}".format(config["file_name"]))

        else:
            app.logger.info("No Valid Scorer found for {}".format(config["file_name"]))
            return "No valid Scorer found"

        return conditions


def get_binary_classification(config, data, conditions):
    micro = {
        "tp_sum": 0,
        "fp_sum": 0,
        "fn_sum": 0,
        "item_sum": 0
    }

    macro = {
        "precision": 0,
        "recall": 0,
        "f1_score": 0,
        "item_sum": 0
    }

    stats = {
        "has_score": 0,
        "no_score": 0,
        "empty_responses": 0
    }

    app.logger.info("Starting Evaluation Calculation for {}".format(config["file_name"]))

    for number, item in data.items():
        # app.logger.debug(f"Evaluating item: {item}")

        if len(item["computed"]) <= 0:
            stats["empty_responses"] += 1
            if config["scorer"]["ignore_empty"]:
                continue

        gold = [entity for entity in item["gold"] if entity["entity_type"] in config["scorer"]["entities"] or
                len(config["scorer"]["entities"]) <= 0]

        computed = [entity for entity in item["computed"] if entity["entity_type"] in config["scorer"]["entities"] or
                    len(config["scorer"]["entities"]) <= 0]

        item_sum = len(gold)

        # app.logger.debug("Gold Entities: {}".format(gold))
        # multiline_logging(app, "Gold Entities: {}".format(gold))
        # app.logger.debug("Computed Entities: {}".format(computed))
        # multiline_logging(app, "Computed Entities: {}".format(computed))

        # Scorer
        confusion_matrix = scorer_lib.get_confusion_matrix(computed, gold, conditions)

        micro["tp_sum"] += confusion_matrix["tp_sum"]
        micro["fp_sum"] += confusion_matrix["fp_sum"]
        micro["fn_sum"] += confusion_matrix["fn_sum"]
        micro["item_sum"] += item_sum

        # Metrics
        precision = metrics_lib.get_precision(confusion_matrix["tp_sum"], confusion_matrix["fp_sum"])
        recall = metrics_lib.get_recall(confusion_matrix["tp_sum"], item_sum)
        f1_score = metrics_lib.get_f1_score(precision, recall)

        macro["precision"] += precision
        macro["recall"] += recall
        macro["f1_score"] += f1_score
        macro["item_sum"] += 1

        data[number]["evaluation"] = {
            "binary_classification": {
                "confusion_matrix": confusion_matrix,
                "item_sum": item_sum,
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
                "entities": ", ".join(config["scorer"]["entities"])
            }
        }

        if f1_score > 0 or precision > 0 or recall > 0:
            stats["has_score"] += 1
        else:
            stats["no_score"] += 1

    # Metrics
    micro["precision"] = metrics_lib.get_precision(micro["tp_sum"], micro["fp_sum"])
    micro["recall"] = metrics_lib.get_recall(micro["tp_sum"], micro["item_sum"])
    micro["f1_score"] = metrics_lib.get_f1_score(micro["precision"], micro["recall"])

    macro["precision"] = macro["precision"] / macro["item_sum"]
    macro["recall"] = macro["recall"] / macro["item_sum"]
    macro["f1_score"] = macro["f1_score"] / macro["item_sum"]

    results = {
        "has_score": stats["has_score"],
        "no_score": stats["no_score"],
        "empty_responses": stats["empty_responses"],
        "entities": ", ".join(config["scorer"]["entities"]),

        "total_tp": micro["tp_sum"],
        "total_fp": micro["fp_sum"],
        "total_fn": micro["fn_sum"],
        "total_item_sum": micro["item_sum"],

        "binary_classification": {
            "micro": {
                "precision": micro["precision"],
                "recall": micro["recall"],
                "f1_score": micro["f1_score"]
            },
            "macro": {
                "precision": macro["precision"],
                "recall": macro["recall"],
                "f1_score": macro["f1_score"]
            }
        }
    }

    app.logger.debug(f'Running {config["evaluator"]["name"]} for {config["file_name"]}')
    app.logger.debug(f'Micro precision = {micro["precision"]}')
    app.logger.debug(f'Micro recall = {micro["recall"]}')
    app.logger.debug(f'Micro f1_score = {micro["f1_score"]}')
    app.logger.debug(f'Macro precision = {macro["precision"]}')
    app.logger.debug(f'Macro recall = {macro["recall"]}')
    app.logger.debug(f'Macro f1_score = {macro["f1_score"]}')

    return data, results
