import json

from application.clients.crawler_client import CrawlerClient
from application.repositories.crawler_repository import CrawlerRepository
from utils.packages.redis.redis_cache import RedisCache


class CrawlerAction:

    def __init__(self, logger, config, redis_cache: RedisCache, crawler_repository: CrawlerRepository,
                 crawler_client: CrawlerClient):
        self._logger = logger
        self._config = config

        self._redis_cache = redis_cache
        self._crawler_repository = crawler_repository
        self._crawler_client = crawler_client

    async def crawl(self, url):
        """Gets the request from the server and pushes it to the repository
        layer, following the defined flow.

        Parameters
        -------
        url
            website to crawl

        Returns
        -------
        Response from the repository or the cached results from Redis
        """

        cached_results = self._redis_cache.get_from_redis(url)
        if cached_results:
            return json.loads(cached_results)

        crawled_results = await self._crawler_repository.crawl(url)
        self._redis_cache.set_to_redis(
            key=url, data=json.dumps(crawled_results), expiration=self._config.REDIS_CONFIG['expiration_timeout'])
        return crawled_results
