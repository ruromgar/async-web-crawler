# Common utils

This folder contains utilities that might be common to all the components in the future:
- Logger
- Redis server

## Logger
No explanation needed - this is just a logger. The config should be provided in the `config.py` file and look like the following:

```
LOG_CONFIG = {
    'name': 'test-name',
    'level': logging.DEBUG,
    'stream_handler': logging.StreamHandler(sys.stdout),
    'format': '%(asctime)s: %(module)s: %(levelname)s: %(message)s'
}
```

## Redis server
A [Redis](https://redis.io/) implementation used for caching. The config should be provided in the `config.py` file and look like the following:

```
REDIS_CONFIG = {
    'hostname': 'redis',
    'port': 6379
}
```