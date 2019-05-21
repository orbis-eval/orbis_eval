from orbis.lib import files

import os


class HTMLOverview(object):
    """docstring for HTMLOverview"""

    def __init__(self, rucksack):
        super(HTMLOverview, self).__init__()
        raise NotImplementedError

        self.rucksack = rucksack
        self.config = self.rucksack["config"]
        self.data = self.rucksack["data"]
        self.results = self.rucksack["results"]

    def run(self) -> None:
        return NotImplementedError
        directory_name = files.build_file_name("html", self.config)
        files.create_folder(directory_name)

        try:
            os.makedirs(directory_name)
        except Exception:
            pass

        file_dir = os.path.join(directory_name, "index.html")
        with open(file_dir, "w") as open_file:
            open_file.write("html")
