from orbis.core import orbis
from orbis.libs import logger
from orbis.libs import files


app = orbis.App()
app.logger = logger.create_logger(app)

# Initialize folders
files.create_folders(app.paths)

# Check if folders are available
files.check_folders(app.paths)
