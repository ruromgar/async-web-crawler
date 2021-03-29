import asyncio

from utils.packages.logger.logger_client import LoggerClient
from utils.packages.redis.redis_cache import RedisCache

from application.actions.crawler_action import CrawlerAction
from application.clients.crawler_client import CrawlerClient
from application.repositories.crawler_repository import CrawlerRepository
from application.server.crawler_server import CrawlerServer
from config import config


class Container:

    def __init__(self):
        self._logger = LoggerClient(config).get_logger()
        self._logger.info("Crawler starting....")

        self._redis_cache = RedisCache(config=config, logger=self._logger)

        self._crawler_client = CrawlerClient(logger=self._logger, config=config)
        self._crawler_repository = CrawlerRepository(
            logger=self._logger, config=config, crawler_client=self._crawler_client)
        self._crawler_action = CrawlerAction(
            logger=self._logger, config=config, redis_cache=self._redis_cache,
            crawler_repository=self._crawler_repository, crawler_client=self._crawler_client)

        self._crawler_server = CrawlerServer(logger=self._logger, config=config, crawler_action=self._crawler_action)

    async def start_server(self):
        await self._crawler_server.run_server()


if __name__ == '__main__':
    container = Container()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(container.start_server(), loop=loop)
    loop.run_forever()
