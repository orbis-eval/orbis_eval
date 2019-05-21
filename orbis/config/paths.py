import os

from orbis.config import settings

# /
source_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))
# /orbis
package_root = os.path.join(source_root, "orbis")
# /queue/activated
queue = os.path.join(source_root, settings.evaluation_configs_dir or "queue", "activated")
# /queue
test_queue = os.path.join(source_root, settings.evaluation_configs_dir or "queue", "tests")
# /data
data_dir = os.path.join(source_root, "data")
# /data/corpora
corpora_dir = os.path.join(data_dir, "corpora")
# /logs
log_path = os.path.join(source_root, "logs")
# /tests
tests_dir = os.path.join(source_root, "tests")
# /output
output_path = os.path.join(source_root, "output")
# /orbis/addons
addons_path = os.path.join(package_root, "addons")
# /orbis/plugins
plugins_path = os.path.join(package_root, "plugins")
