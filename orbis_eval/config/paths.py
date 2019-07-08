# -*- coding: utf-8 -*-

import json
import os

# /
source_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
# /orbis
package_root = os.path.join(source_root, 'orbis_eval')
# /orbis/config/settings.json
settings_file = os.path.join(package_root, 'config', 'settings.json')
# /orbis/config/user_folder.txt
user_folder_settings_file = os.path.join(package_root, 'config', 'user_folder.txt')
# /tests
tests_dir = os.path.join(source_root, 'tests')
# Load config as dict
with open(settings_file, 'r', encoding='utf-8') as open_file:
    config = json.load(open_file)
# ~/orbis-eval
with open(user_folder_settings_file, 'r', encoding='utf-8') as open_file:
    user_dir = open_file.read()
# /data
data_dir = os.path.join(user_dir, 'data')
# /data/corpora
corpora_dir = os.path.join(data_dir, 'corpora')
# /logs
log_path = os.path.join(user_dir, 'logs')
# /queue/activated
queue = os.path.join(user_dir, config['queue'] or 'queue', 'activated')
# /queue/tests
test_queue = os.path.join(user_dir, config['queue'] or 'queue', 'tests')
# /output
output_path = os.path.join(user_dir, 'output')
# /orbis/addons
addons_path = os.path.join(package_root, 'addons')
# /orbis/plugins
plugins_path = os.path.join(package_root, 'plugins')
