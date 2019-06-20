
import collections
import os
import csv

from orbis import app
from orbis.libs import files


class ListResults(object):
    """docstring for ListResults"""

    def __init__(self, rucksack):
        super(ListResults, self).__init__()
        raise NotImplementedError

        self.rucksack = rucksack
        self.config = self.rucksack["config"]
        self.results = self.rucksack["results"]

    def run(self):
        app.logger.info("Saving results as csv.")

        file_name = files.build_file_name("collected_results.csv", self.config, raw=True)

        response = collections.OrderedDict()
        response["date"] = files.get_timestamp()
        response["name"] = self.config["file_name"]

        response["macro_precision"] = self.results["binary_classification"]["macro"]["precision"]
        response["macro_recall"] = self.results["binary_classification"]["macro"]["recall"]
        response["macro_f1_score"] = self.results["binary_classification"]["macro"]["f1_score"]

        response["micro_precision"] = self.results["binary_classification"]["micro"]["precision"]
        response["micro_recall"] = self.results["binary_classification"]["micro"]["recall"]
        response["micro_f1_score"] = self.results["binary_classification"]["micro"]["f1_score"]

        response["has_score"] = self.results["has_score"]
        response["no_score"] = self.results["no_score"]
        response["empty_responses"] = self.results["empty_responses"]

        response["aggregator_name"] = self.config["aggregator"]["service"]["name"]
        response["aggregator_profile"] = self.config["aggregator"]["service"].get("profile", "None")
        response["aggregator_limit"] = self.config["aggregator"]["service"].get("limit", "None")
        response["aggregator_location"] = self.config["aggregator"]["service"]["location"]
        response["aggregator_data_set"] = self.config["aggregator"]["input"]["data_set"]["name"]

        response["evaluator_name"] = self.config["evaluator"]["name"]
        response["scorer_name"] = self.config["scorer"]["name"]

        response["entities"] = " ".join([e for e in self.config["scorer"]["entities"]])
        response["mapping"] = self.config["aggregator"]["input"].get("mappings", "None")
        response["lense"] = self.config["aggregator"]["input"].get("lenses", "None")
        response["filter"] = self.config["aggregator"]["input"].get("filters", "None")

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
