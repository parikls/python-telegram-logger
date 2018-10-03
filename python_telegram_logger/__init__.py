import logging

# configure root logger
root_logger = logging.getLogger()
formatter = logging.Formatter('python-telegram-logger : %(levelname)s: %(module)s: %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)

from .handlers import *
from .formatters import *
