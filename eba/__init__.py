from corelog import register
from os import environ

__name__ = "eba"

register(environ.get("EBA_LOG_LEVEL", "INFO"))
