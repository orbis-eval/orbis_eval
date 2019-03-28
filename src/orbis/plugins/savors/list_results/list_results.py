from orbis import app
from orbis.libs.files_lib import build_file_name
from orbis.libs.files_lib import get_timestamp

import collections
import os
import csv


def run(yaml_config: dict, data: dict, results: dict):
    app.logger.info("Saving results as csv.")

    file_name = build_file_name("collected_results.csv", yaml_config, raw=True)

    response = collections.OrderedDict()
    response["date"] = get_timestamp()
    response["name"] = yaml_config["file_name"]

    response["macro_precision"] = results["binary_classification"]["macro"]["precision"]
    response["macro_recall"] = results["binary_classification"]["macro"]["recall"]
    response["macro_f1_score"] = results["binary_classification"]["macro"]["f1_score"]

    response["micro_precision"] = results["binary_classification"]["micro"]["precision"]
    response["micro_recall"] = results["binary_classification"]["micro"]["recall"]
    response["micro_f1_score"] = results["binary_classification"]["micro"]["f1_score"]

    response["has_score"] = results["has_score"]
    response["no_score"] = results["no_score"]
    response["empty_responses"] = results["empty_responses"]

    response["aggregator_name"] = yaml_config["aggregator"]["service"]["name"]
    response["aggregator_profile"] = yaml_config["aggregator"]["service"].get("profile", "None")
    response["aggregator_limit"] = yaml_config["aggregator"]["service"].get("limit", "None")
    response["aggregator_location"] = yaml_config["aggregator"]["service"]["location"]
    response["aggregator_data_set"] = yaml_config["aggregator"]["input"]["data_set"]["name"]

    response["evaluator_name"] = yaml_config["evaluator"]["name"]
    response["scorer_name"] = yaml_config["scorer"]["name"]

    response["entities"] = " ".join([e for e in yaml_config["scorer"]["entities"]])
    response["mapping"] = yaml_config["aggregator"]["input"].get("mappings", "None")
    response["lense"] = yaml_config["aggregator"]["input"].get("lenses", "None")
    response["filter"] = yaml_config["aggregator"]["input"].get("filters", "None")

    header = [key for key in response.keys()]
    values = [value for value in response.values()]

    if not os.path.isfile(file_name):
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t', quotechar="'")
            writer.writerow(header)

    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quotechar="'")
        writer.writerow(values)

    app.logger.info("Finished saving results as csv.")
