import logging
import sys


format = "%(asctime)-15s %(threadName)s %(module)s %(funcName)s %(lineno)d %(message)s"

logging.basicConfig(format=format, stream=sys.stderr, level=logging.DEBUG)
db_log = logging.getLogger(__name__)

for handler in logging.root.handlers:
    handler.addFilter(logging.Filter(__name__))