# -*- coding: utf-8 -*-

import os


class AddonBaseClass(object):
    """docstring for AddonBaseClass"""

    def __init__(self):
        super(AddonBaseClass, self).__init__()
        self.addon_path = None

    def get_description(self):
        self.description_path = os.path.join(self.addon_path, "description.txt")
        try:
            with open(self.description_path, "r", encoding="utf-8") as open_file:
                self.description = open_file.read().strip()
        except Exception as exception:
            print(exception)
            self.description = None
