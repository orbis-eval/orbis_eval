#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import os
from orbis.config import settings


source_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))
package_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
evaluation_configs_dir = os.path.join(source_root, settings.evaluation_configs_dir or "evaluation_configs", "activated")
data_dir = os.path.join(source_root, "data")
corpora_dir = os.path.join(data_dir, "corpora")
log_path = os.path.join(source_root, "logs")
tests_dir = os.path.join(source_root, "tests")
output_path = os.path.join(source_root, "output")
addons_path = os.path.join(package_root, "addons")
plugins_path = os.path.join(package_root, "plugins")
