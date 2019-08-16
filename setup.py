# -*- coding: utf-8 -*-
try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from pathlib import PurePath

import re
import io
import os
import sys


class OrbisSetup(object):
    """docstring for OrbisSetup"""

    def __init__(self):
        super(OrbisSetup, self).__init__()
        self.extras = {
            'all': [
                "orbis_plugin_aggregation_dbpedia_entity_types",
                "orbis_plugin_aggregation_monocle",
                "orbis_plugin_aggregation_gold_gs",
                "orbis_plugin_aggregation_serial_corpus",
                "orbis_plugin_aggregation_local_cache",
                "orbis_plugin_aggregation_aida",
                "orbis_plugin_aggregation_babelfly",
                "orbis_plugin_aggregation_spotlight",
                "orbis_plugin_evaluation_binary_classification_evaluation",
                "orbis_plugin_metrics_binary_classification_metrics",
                "orbis_plugin_scoring_nel_scorer",
                "orbis_plugin_storage_cache_webservice_results",
                "orbis_plugin_storage_csv_result_list",
                "orbis_plugin_storage_html_pages",
                "orbis_plugin_storage_single_view",
                "orbis_addon_tunnelblick",
                "orbis_addon_satyanweshi",
                "orbis_addon_repoman"
            ]
        }

    def load_requirements_file(self, plugin_name, metadata, dev):
        requirements = ["orbis_eval"] if metadata["type"] != "main" else []
        with open(metadata['requirements_file'], encoding="utf8") as open_file:
            for line in open_file.readlines():
                if dev:
                    line = line.replace("\n", "").replace(
                        "<", "=").replace(">", "=")
                    line = line.split("=")[0]
                    requirements.append(line)
                else:
                    requirements.append(line.replace("\n", ""))
        return requirements

    def check_python_version(self, metadata):
        python_needed = tuple(
            [int(i) for i in metadata['min_python_version'].split(".")])
        if not sys.version_info >= python_needed:
            sys.exit(
                f"Sorry, Python {metadata['min_python_version']} or newer needed")

    def get_long_description(self):
        with io.open("README.md", "rt", encoding="utf8") as f:
            long_description = f.read()
        return long_description

    def parse_metadata(self, target, file_content):
        regex = f"^{target} = ['\"](.*?)['\"]"
        metadatum = re.search(regex, file_content, re.MULTILINE).group(1)
        return metadatum

    def load_metadata(self, directory, plugin_name):
        metadata = {}

        with io.OpenWrapper(f"{directory}/{plugin_name}/__init__.py", "rt", encoding="utf8") as open_file:
            file_content = open_file.read()

        metadata["version"] = self.parse_metadata("__version__", file_content)
        metadata["name"] = self.parse_metadata("__name__", file_content)
        metadata["author"] = self.parse_metadata("__author__", file_content)
        metadata["description"] = self.parse_metadata(
            "__description__", file_content)
        metadata["license"] = self.parse_metadata("__license__", file_content)
        metadata["min_python_version"] = self.parse_metadata(
            "__min_python_version__", file_content)
        metadata["requirements_file"] = self.parse_metadata(
            "__requirements_file__", file_content)
        metadata["url"] = self.parse_metadata("__url__", file_content)
        metadata["year"] = self.parse_metadata("__year__", file_content)
        metadata["type"] = self.parse_metadata("__type__", file_content)

        return metadata

    def get_extras(self):
        extras = self.extras
        for extra in extras["all"]:
            extra_parts = extra.split("_")

            if extra_parts[1] == "plugin":
                extra_parts[1] = "all_plugins"
                extra_parts[3] = "_".join(extra_parts[3:])
                extra_parts = extra_parts[1:4]

            if extra_parts[1] == "addon":
                extra_parts[1] = "all_addons"
                extra_parts[2] = "_".join(extra_parts[2:])
                extra_parts = extra_parts[1:3]

            for part in extra_parts:
                extras[part] = extras.get(part, []) + [extra]

        return extras

    def run(self, directory):

        plugin_name = PurePath(directory).parts[-1]
        metadata = self.load_metadata(directory, plugin_name)
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
            "package_data": {'orbis_eval': [
                'config/settings.json',
                'data/tests/queue/*',
                'data/tests/corpora/rss1/computed/**/*',
                'data/tests/corpora/rss1/**/*'
            ]
            }
        }

        if metadata["type"] == "main":
            print("Main found. Installing entry points.")
            setup_dict["entry_points"] = {
                'console_scripts': [
                    'orbis-eval = orbis_eval.__main__:run',
                    'orbis-addons = orbis_eval.interfaces.addons.main:run'
                ]
            }

        setup_dict["extras_require"] = self.get_extras()

        setup(**setup_dict)


if __name__ == '__main__':
    directory = os.path.dirname(os.path.realpath(__file__))
    OrbisSetup().run(directory)
