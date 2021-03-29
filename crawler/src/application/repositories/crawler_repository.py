from application.clients.crawler_client import CrawlerClient


class CrawlerRepository:

    def __init__(self, logger, config, crawler_client: CrawlerClient):
        self._logger = logger
        self._config = config
        self._crawler_client = crawler_client

    async def crawl(self, url):
        """Gets the request from the server and pushes it to the client
        layer, following the defined flow.

        Parameters
        -------
        url
            website to crawl

        Returns
        -------
        Response from the client.
        """

        return await self._crawler_client.start_crawler(url)
