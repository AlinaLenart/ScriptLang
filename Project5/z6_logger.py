import logging
import sys

# creating logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  

# handler for stdout (DEBUG, INFO, WARNING)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

# handler for stderr (ERROR)
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)

# format of logs
formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

# adding handlers to logger
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)