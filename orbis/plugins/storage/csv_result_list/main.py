"""Summary
"""
import csv
import os

from orbis import app
from orbis.libs import files
from orbis.libs import storage


class CSVResultList(object):

    def __init__(self, rucksack):
        super(CSVResultList, self).__init__()
        self.rucksack = rucksack
        self.pass_name = self.rucksack.open['config']['file_name'].split(".")[0]
        self.folder = os.path.join(app.paths.output_path, "csv_result_list")
        self.file_name = os.path.join(self.folder, "results.csv")
        files.create_folder(self.folder)

    def run(self):
        app.logger.info("Saving results to csv overview")
        response = {
            'date': files.get_timestamp(),
            'aggregator_name': self.rucksack.open['config']['aggregation']['service']['name'],
            'aggregator_profile': self.rucksack.open['config']['aggregation']['service'].get('profile', 'None'),
            'aggregator_limit': self.rucksack.open['config']['aggregation']['service'].get('limit', 'None'),
            'aggregator_service': self.rucksack.open['config']['aggregation']['service']['name'],
            'aggregator_data_set': self.rucksack.open['config']['aggregation']['input']['data_set']['name'],
            'evaluator_name': self.rucksack.open['config']['evaluation']['name'],
            'scorer_name': self.rucksack.open['config']['scoring']['name']
        }
        for key, value in storage.flatten(self.rucksack.open['results']).items():
            response[key] = value
        header = [key for key, value in response.items()]
        values = [value for key, value in response.items()]
        try:
            with open(self.file_name, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar="'")
                first_row = next(reader)
        except FileNotFoundError:
            first_row = None
        # check if not allready csv
        with open(self.file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar="'")
            if first_row != header:
                writer.writerow(header)
            writer.writerow(values)
        app.logger.info("Finished saving results to csv overview")
