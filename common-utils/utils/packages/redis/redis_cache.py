import logging
import sys

from redis import Redis


class RedisCache:
    _config = None
    _logger = None

    def __init__(self, config, logger=None):
        self._config = config

        if logger is None:
            logger = logging.getLogger('redis')
            logger.setLevel(logging.DEBUG)
            log_handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s: %(module)s: %(levelname)s: %(message)s')
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)
        self._logger = logger

        self._redis_connection_string = \
            f"redis://{self._config.REDIS_CONFIG['hostname']}:{self._config.REDIS_CONFIG['port']}"
        self._redis_engine = self.__get_redis_engine()

    def __get_redis_engine(self):
        try:
            return Redis.from_url(self._redis_connection_string, encoding="utf-8", decode_responses=True)
        except Exception as e:
            self._logger.error(f'Redis is not connecting. Error: {e}')
            return None

    def get_from_redis(self, key):
        try:
            return self._redis_engine.get(key)
        except Exception as e:
            self._logger.info(f'Redis is not working on get hash {key} with the following error - {e}')
            return None

    def set_to_redis(self, key, data, expiration=0):
        try:
            if expiration == 0:
                self._redis_engine.set(key, data)
            else:
                self._redis_engine.set(key, data, ex=expiration)

        except Exception as e:
            self._logger.info(f'Redis is not working on set hash {key} with the following error - {e}')
