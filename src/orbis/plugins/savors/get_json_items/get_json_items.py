from orbis import app
from orbis.libs.files_lib import build_file_name

import json


def run(yaml_config: dict, data: dict, results: dict):
    app.logger.info("Saving seperate data as json.")
    file_name = build_file_name("json_items.json", yaml_config)

    dump = {
        "yaml_config": yaml_config,
        "data": data,
        "results": results
    }

    with open(file_name, "w") as open_file:
        json.dump(dump, open_file, indent=4, sort_keys=True)

    """
    if config["savor"]["json_items"].get("print"):
        pprint(data)
    """

    app.logger.info("Finished saving seperate data as json.")
