import json

from orbis import app
from orbis.libs.files_lib import build_file_name
from orbis.libs.files_lib import get_timestamp
from orbis.libs.savor_lib import flatten
import collections


def run(yaml_config: dict, data: dict, results: dict):
    app.logger.info("Saving results as json.")

    json_response = {
        "date": get_timestamp(),
        "aggregator_name": yaml_config["aggregator"]["service"]["name"],
        "aggregator_profile": yaml_config["aggregator"]["service"].get("profile", "None"),
        "aggregator_limit": yaml_config["aggregator"]["service"].get("limit", "None"),
        "aggregator_location": yaml_config["aggregator"]["service"]["location"],
        "aggregator_data_set": yaml_config["aggregator"]["input"]["data_set"]["name"],
        "evaluator_name": yaml_config["evaluator"]["name"],
        "scorer_name": yaml_config["scorer"]["name"]
    }

    for key, value in flatten(results).items():
        json_response[key] = value

    file_name = build_file_name("json_results.json", yaml_config)

    with open(file_name, "w") as open_file:
        json.dump(json_response, open_file, indent=4, sort_keys=True)

    app.logger.info("Finished saving results as json.")
