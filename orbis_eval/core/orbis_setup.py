# -*- coding: utf-8 -*-

from pathlib import PurePath
from setuptools import find_packages
from setuptools import setup
import io
import os
import sys

from orbis_eval.libs import orbis_setup


class OrbisSetupBaseClass(object):
    """docstring for OrbisSetupBaseClass"""

    def __init__(self, setup_dict=None):
        super(OrbisSetupBaseClass, self).__init__()
        self.setup_dict = setup_dict or {}

    def load_requirements_file(self, plugin_name, metadata, dev):
        # requirements = ["orbis_eval"] if metadata["type"] != "main" else []
        requirements = []
        with open(metadata['requirements_file'], encoding="utf8") as open_file:
            for line in open_file.readlines():
                if dev:
                    line = line.replace("\n", "").replace("<", "=").replace(">", "=")
                    line = line.split("=")[0]
                    requirements.append(line)
                else:
                    requirements.append(line.replace("\n", ""))
        return requirements

    def check_python_version(self, metadata):
        python_needed = tuple([int(i) for i in metadata['min_python_version'].split(".")])
        if not sys.version_info >= python_needed:
            sys.exit(f"Sorry, Python {metadata['min_python_version']} or newer needed")

    def get_long_description(self):
        with io.open("README.md", "rt", encoding="utf8") as f:
            long_description = f.read()
        return long_description

    def add_to_setup_dict(self, setup_dict):
        setup_dict.update(self.additional_setup_dict)
        return setup_dict

    def run(self, directory):

        path_split = PurePath(directory).parts
        plugin_name = path_split[-1]

        metadata = orbis_setup.load_metadata(f"{directory}/{plugin_name}/__init__.py")
        self.check_python_version(metadata)

        dev = False  # Dev set ignores requirements versions

        setup_dict = {
            "name": metadata['name'],
            "author": metadata['author'],
            "version": metadata['version'],
            "description": metadata['description'],
            "long_description": self.get_long_description(),
            "long_description_content_type": 'text/markdown',
            "url": metadata['url'],
            "license": metadata['license'],
            "packages": find_packages(),
            "python_requires": f">{metadata['min_python_version']}",
            "install_requires": self.load_requirements_file(plugin_name, metadata, dev),
            "include_package_data": True
        }

        setup_dict.update(self.setup_dict)

        setup(**setup_dict)


if __name__ == '__main__':
    directory = os.path.dirname(os.path.realpath(__file__))
    OrbisSetupBaseClass().run(directory)
