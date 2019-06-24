#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import json
import os

# /
source_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
# /orbis
package_root = os.path.join(source_root, 'orbis')
# /orbis/config/settings.json
settings_file = os.path.join(package_root, 'config', 'settings.json')

# /tests
tests_dir = os.path.join(source_root, 'tests')

with open(settings_file, 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# ~/orbis-eval
user_dir = config['user_dir'] or source_root
# /data
data_dir = os.path.join(user_dir, 'data')
# /data/corpora
corpora_dir = os.path.join(data_dir, 'corpora')
# /logs
log_path = os.path.join(user_dir, 'logs')
# /queue/activated
queue = os.path.join(user_dir, config['queue'] or 'queue', 'activated')
# /queue/tests
test_queue = os.path.join(source_root, config['queue'] or 'queue', 'tests')
# /output
output_path = os.path.join(user_dir, 'output')
# /orbis/addons
addons_path = os.path.join(package_root, 'addons')
# /orbis/plugins
plugins_path = os.path.join(package_root, 'plugins')
print(user_dir)
