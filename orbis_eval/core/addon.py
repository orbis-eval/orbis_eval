# -*- coding: utf-8 -*-

import os

from orbis_eval.libs import orbis_setup


class AddonBaseClass(object):
    """docstring for AddonBaseClass"""

    def __init__(self):
        super(AddonBaseClass, self).__init__()
        self.addon_path = None
        self.metadata = self.load_metadata()

    def get_description(self):
        init_path = os.path.join(self.addon_path, '__init__.py')
        self.description = orbis_setup.load_metadata(init_path)['description']
