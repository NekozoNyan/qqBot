import logging
import sys


_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(
    logging.Formatter('[%(asctime)s %(name)s] %(levelname)s: %(message)s')
)

logger = logging.getLogger('neko')
logger.addHandler(_handler)
logger.setLevel(logging.INFO)