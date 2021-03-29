import logging
import os
import sys

WORKSPACE = os.environ["WORKSPACE"]

LOG_CONFIG = {
    'name': 'crawler',
    'level': logging.DEBUG,
    'stream_handler': logging.StreamHandler(sys.stdout),
    'format': '%(asctime)s: %(module)s: %(levelname)s: %(message)s'
}

REDIS_CONFIG = {
    'hostname': os.environ['REDIS_HOSTNAME'],
    'port': os.environ['REDIS_PORT'],
    'expiration_timeout': 300,
}

FASTAPI_CONFIG = {
    'port': 8081,
}

MAX_CONCURRENT_REQUESTS = 20
