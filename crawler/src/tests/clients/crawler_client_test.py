from unittest.mock import Mock
from unittest.mock import patch

import pytest
from application.clients.crawler_client import CrawlerClient
from asynctest import CoroutineMock
from config import test_config as config


class TestCrawlerClient:

    def instance_test(self):
        logger = Mock()
        crawler_client = CrawlerClient(logger, config)

        assert crawler_client._config is config
        assert crawler_client._logger is logger

    @pytest.mark.asyncio
    async def start_crawler_OK_test(self):
        logger = Mock()
        crawler_client = CrawlerClient(logger, config)

        base_url = 'www.someurl.com'
        domain = 'someurl'
        page_map = 'a map'
        crawled_results = [(base_url, 'www.crawled.com')]

        crawler_client.extract_domain_from_url = Mock(return_value=domain)
        crawler_client.build_page_map = Mock(return_value=page_map)
        crawler_client.crawl = CoroutineMock(return_value=crawled_results)

        results = await crawler_client.start_crawler(base_url)

        crawler_client.extract_domain_from_url.assert_called_once()
        crawler_client.build_page_map.assert_called()
        crawler_client.crawl.assert_called()
        assert results == page_map

    @pytest.mark.asyncio
    async def start_crawler_KO_invalid_url_test(self):
        logger = Mock()
        crawler_client = CrawlerClient(logger, config)

        base_url = 'www.someurl.com'
        page_map = 'a map'
        crawled_results = [(base_url, 'www.crawled.com')]

        crawler_client.extract_domain_from_url = Mock(return_value=None)
        crawler_client.build_page_map = Mock(return_value=page_map)
        crawler_client.crawl = CoroutineMock(return_value=crawled_results)

        results = await crawler_client.start_crawler(base_url)

        crawler_client.extract_domain_from_url.assert_called_once()
        crawler_client.build_page_map.assert_not_called()
        crawler_client.crawl.assert_not_called()
        assert results is None

    @pytest.mark.asyncio
    async def crawl_OK_test(self):
        logger = Mock()
        crawler_client = CrawlerClient(logger, config)

        item = ('parent_url', 'www.someurl.com')
        domain = 'someurl'

        crawled_results = '<a><href>www.resulturl.com</href></a>'
        full_url = 'www.resulturl.com'

        response_mock = CoroutineMock()
        response_mock.text = CoroutineMock(return_value=crawled_results)

        with patch.object(crawler_client._session, 'get', new=CoroutineMock(return_value=response_mock)) as mock_get:

            crawler_client.build_full_url = Mock(return_value=full_url)
            results = await crawler_client.crawl(item, domain)

        mock_get.assert_called_once()
        assert results == [('www.someurl.com', 'www.resulturl.com')]

    @pytest.mark.asyncio
    async def crawl_KO_domain_not_in_url_test(self):
        logger = Mock()
        crawler_client = CrawlerClient(logger, config)

        item = ('parent_url', 'www.someurl.com')
        domain = 'some_other_url'

        crawled_results = '<a><href>www.resulturl.com</href></a>'
        full_url = 'www.resulturl.com'

        response_mock = CoroutineMock()
        response_mock.text = CoroutineMock(return_value=crawled_results)

        with patch.object(crawler_client._session, 'get', new=CoroutineMock(return_value=response_mock)) as mock_get:

            crawler_client.build_full_url = Mock(return_value=full_url)
            results = await crawler_client.crawl(item, domain)

        mock_get.assert_not_called()
        assert results == []

    def extract_domain_from_url_test(self):
        logger = Mock()
        crawler_client = CrawlerClient(logger, config)

        url_1 = 'https://www.someurl.com'
        expected_domain_1 = 'www.someurl.com'

        url_2 = 'notavalidurl.com'
        expected_domain_2 = None

        result1 = crawler_client.extract_domain_from_url(url_1)
        result2 = crawler_client.extract_domain_from_url(url_2)

        assert expected_domain_1 == result1
        assert expected_domain_2 == result2

    def build_full_url_test(self):
        logger = Mock()
        crawler_client = CrawlerClient(logger, config)

        base_url_1 = 'https://www.someurl.com'
        child_url_1 = 'https://www.someurl.com/submit'
        expected_url_1 = 'https://www.someurl.com/submit'

        base_url_2 = 'https://www.someurl.com'
        child_url_2 = 'submit'
        expected_url_2 = 'https://www.someurl.com/submit'

        result1 = crawler_client.build_full_url(base_url_1, child_url_1)
        result2 = crawler_client.build_full_url(base_url_2, child_url_2)

        assert expected_url_1 == result1
        assert expected_url_2 == result2

    def build_page_map_test(self):
        logger = Mock()
        crawler_client = CrawlerClient(logger, config)

        page_map_1 = {'A': {}}
        parent_1 = 'A'
        url_1 = 'B'
        expected_page_map_1 = {'A': {'B': {}}}

        page_map_2 = {'A': {'B': {'F': {}, 'C': {}}, 'C': {}, 'D': {}}}
        parent_2 = 'F'
        url_2 = 'I'
        expected_page_map_2 = {'A': {'B': {'F': {'I': {}}, 'C': {}}, 'C': {}, 'D': {}}}

        page_map_3 = {'A': {}}
        parent_3 = None
        url_3 = 'Whatever'
        expected_page_map_3 = {'A': {}}

        result1 = crawler_client.build_page_map(page_map_1, parent_1, url_1)
        result2 = crawler_client.build_page_map(page_map_2, parent_2, url_2)
        result3 = crawler_client.build_page_map(page_map_3, parent_3, url_3)

        assert expected_page_map_1 == result1
        assert expected_page_map_2 == result2
        assert expected_page_map_3 == result3
