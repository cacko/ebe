from corelog import register
from os import environ

__name__ = "ebe"

register(environ.get("EBE_LOG_LEVEL", "INFO"))
