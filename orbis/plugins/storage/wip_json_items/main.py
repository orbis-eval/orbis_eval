from orbis import app
from orbis.libs import files

import json


class JSONItems(object):
    """docstring for JSONItems"""

    def __init__(self, rucksack):
        super(JSONItems, self).__init__()
        raise NotImplementedError

        self.rucksack = rucksack
        self.config = self.rucksack["config"]
        self.data = self.rucksack["data"]
        self.results = self.rucksack["results"]

    def run(self):
        app.logger.info("Saving seperate data as json.")
        file_name = files.build_file_name("json_items.json", self.config)

        dump = {
            "yaml_config": self.config,
            "data": self.data,
            "results": self.results
        }

        with open(file_name, "w") as open_file:
            json.dump(dump, open_file, indent=4, sort_keys=True)

        """
        if config["savor"]["json_items"].get("print"):
            pprint(data)
        """

        app.logger.info("Finished saving seperate data as json.")
