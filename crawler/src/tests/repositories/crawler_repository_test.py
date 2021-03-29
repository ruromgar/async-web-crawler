from unittest.mock import Mock

import pytest
from application.repositories.crawler_repository import CrawlerRepository
from asynctest import CoroutineMock
from config import test_config as config


class TestCrawlerRepository:

    def instance_test(self):
        logger = Mock()
        crawler_client = Mock()

        crawler_repository = CrawlerRepository(logger, config, crawler_client)

        assert crawler_repository._config is config
        assert crawler_repository._logger is logger
        assert crawler_repository._crawler_client is crawler_client

    @pytest.mark.asyncio
    async def crawl_test(self):
        logger = Mock()
        crawler_client = Mock()

        url = 'www.someurl.com'
        crawled_results = 'some results'

        crawler_client.start_crawler = CoroutineMock(return_value=crawled_results)

        crawler_repository = CrawlerRepository(logger, config, crawler_client)

        results = await crawler_repository.crawl(url)

        crawler_client.start_crawler.assert_called_once()
        assert results == crawled_results
