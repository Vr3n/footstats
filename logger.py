import logging
import sys

logger = logging.getLogger()


formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
)


# Create handlers.
stream_handler = logging.StreamHandler(
    sys.stdout
)
file_handler = logging.FileHandler('app.log')

# set formatters.
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handlers to the logger.
logger.handlers = [stream_handler, file_handler]


# set log-level
logger.setLevel(logging.INFO)
