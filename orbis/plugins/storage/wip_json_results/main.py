import json

from orbis import app
from orbis.lib import files


class JSONResults(object):
    """docstring for JSONResults"""

    def __init__(self, rucksack):
        super(JSONResults, self).__init__()
        raise NotImplementedError

        self.rucksack = rucksack
        self.config = self.rucksack["config"]
        self.data = self.rucksack["data"]
        self.results = self.rucksack["results"]

    def run(self):
        app.logger.info("Saving results as json.")

        json_response = {
            "date": files.get_timestamp(),
            "aggregator_name": self.config["aggregator"]["service"]["name"],
            "aggregator_profile": self.config["aggregator"]["service"].get("profile", "None"),
            "aggregator_limit": self.config["aggregator"]["service"].get("limit", "None"),
            "aggregator_location": self.config["aggregator"]["service"]["location"],
            "aggregator_data_set": self.config["aggregator"]["input"]["data_set"]["name"],
            "evaluator_name": self.config["evaluator"]["name"],
            "scorer_name": self.config["scorer"]["name"]
        }

        for key, value in files.flatten(self.results).items():
            json_response[key] = value

        file_name = files.build_file_name("json_results.json", self.config)

        with open(file_name, "w") as open_file:
            json.dump(json_response, open_file, indent=4, sort_keys=True)

        app.logger.info("Finished saving results as json.")
