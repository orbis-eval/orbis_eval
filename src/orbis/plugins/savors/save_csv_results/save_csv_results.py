from orbis import app
from orbis.libs.files_lib import build_file_name
from orbis.libs.files_lib import get_timestamp
from orbis.libs.savor_lib import flatten

import csv


def run(yaml_config: dict, data: dict, results: dict):
    app.logger.info("Saving results to csv overview")
    file_name = build_file_name("csv_results.csv", yaml_config, raw=True)

    response = {
        "date": get_timestamp(),
        "aggregator_name": yaml_config["file_name"].split(".")[0],
        "aggregator_profile": yaml_config["aggregator"]["service"].get("profile", "None"),
        "aggregator_limit": yaml_config["aggregator"]["service"].get("limit", "None"),
        "aggregator_service": yaml_config["aggregator"]["service"]["name"],
        "aggregator_data_set": yaml_config["aggregator"]["input"]["data_set"],
        "evaluator_name": yaml_config["evaluator"]["name"],
        "scorer_name": yaml_config["scorer"]["name"]
    }

    for key, value in flatten(results).items():
        response[key] = value

    header = [key for key, value in response.items()]
    values = [value for key, value in response.items()]

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar="'")
        writer.writerow(header)
        writer.writerow(values)
    app.logger.info("Finished saving results to csv overview")
