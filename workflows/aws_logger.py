import logging
import watchtower

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())