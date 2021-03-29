import logging
import sys

LOG_CONFIG = {
    'name': 'crawler-test',
    'level': logging.DEBUG,
    'stream_handler': logging.StreamHandler(sys.stdout),
    'format': '%(asctime)s: %(module)s: %(levelname)s: %(message)s'
}

REDIS_CONFIG = {
    'hostname': 'redis',
    'port': 6379,
    'expiration_timeout': 300,
}

FASTAPI_CONFIG = {
    'port': 8081,
}

MAX_CONCURRENT_REQUESTS = 20
