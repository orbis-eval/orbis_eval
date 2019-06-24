from orbis.core import orbis
from orbis.libs import logger


app = orbis.App()
app.logger = logger.create_logger(app)
