from unittest.mock import Mock

import pytest
from application.server.crawler_server import CrawlerServer
from asynctest import CoroutineMock
from config import test_config as config
from fastapi import HTTPException
from pytest import raises


class TestCrawlerServer:

    def instance_test(self):
        logger = Mock()
        crawler_action = Mock()

        crawler_server = CrawlerServer(logger, config, crawler_action)

        assert crawler_server._logger is logger
        assert crawler_server._config is config
        assert crawler_server._crawler_action is crawler_action

    def healthcheck_test(self):
        logger = Mock()
        crawler_action = Mock()

        crawler_server = CrawlerServer(logger, config, crawler_action)

        response = crawler_server.healthcheck()

        assert response == {"status": 200}

    @pytest.mark.asyncio
    async def crawl_OK_test(self):
        logger = Mock()
        crawler_action = Mock()

        url = 'https://www.avalidurl.com'
        crawled_results = 'some results'

        crawler_action.crawl = CoroutineMock(return_value=crawled_results)

        crawler_server = CrawlerServer(logger, config, crawler_action)

        result = await crawler_server.crawl(url)
        assert result == crawled_results

    @pytest.mark.asyncio
    async def crawl_KO_invalid_url_test(self):
        logger = Mock()
        crawler_action = Mock()

        url = 'http.notavalidurl.com'

        crawler_action.crawl = CoroutineMock()

        crawler_server = CrawlerServer(logger, config, crawler_action)

        with raises(HTTPException):
            result = await crawler_server.crawl(url)
            assert result is None
