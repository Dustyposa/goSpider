import sys

from loguru import logger

logger.add(sys.stdout, serialize=True)
logger.info("this is a logger")
