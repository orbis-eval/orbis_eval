"""Summary
"""
import os
import json

from orbis import app
from orbis.libs import files


class CacheWebserviceResults(object):

    def __init__(self, rucksack):
        super(CacheWebserviceResults, self).__init__()
        self.rucksack = rucksack
        self.config = self.rucksack.open["config"]

    def run(self):
        data_set_name = self.config["aggregation"]["input"]["data_set"]["name"]
        data_set_path = os.path.join(app.paths.corpora_dir, data_set_name)
        service_name = self.config["aggregation"]["service"]["name"]
        path = os.path.join(data_set_path, "computed", service_name)
        files.create_folder(path)
        for item in self.rucksack.itemsview():
            file_name = os.path.join(path, str(item['index']) + ".json")
            print(file_name)
            with open(file_name, "w") as open_file:
                json.dump(item["computed"], open_file)
