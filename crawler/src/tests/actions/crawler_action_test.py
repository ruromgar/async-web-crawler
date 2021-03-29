import json
from unittest.mock import Mock

import pytest
from application.actions.crawler_action import CrawlerAction
from asynctest import CoroutineMock
from config import test_config as config


class TestCrawlerAction:

    def instance_test(self):
        logger = Mock()
        redis_cache = Mock()
        crawler_repository = Mock()
        crawler_client = Mock()

        redis_cache.get_from_redis = Mock(return_value='Not none')

        crawler_action = CrawlerAction(logger, config, redis_cache, crawler_repository, crawler_client)

        assert crawler_action._config is config
        assert crawler_action._logger is logger
        assert crawler_action._redis_cache is redis_cache
        assert crawler_action._crawler_repository is crawler_repository
        assert crawler_action._crawler_client is crawler_client

    @pytest.mark.asyncio
    async def crawl_OK_no_cached_results_test(self):
        logger = Mock()
        redis_cache = Mock()
        crawler_repository = Mock()
        crawler_client = Mock()

        url = 'www.someurl.com'
        crawled_results = 'some results'

        redis_cache.get_from_redis = Mock(return_value=None)
        redis_cache.set_to_redis = Mock()
        crawler_repository.crawl = CoroutineMock(return_value=crawled_results)

        crawler_action = CrawlerAction(logger, config, redis_cache, crawler_repository, crawler_client)

        result = await crawler_action.crawl(url)

        redis_cache.get_from_redis.assert_called_once()
        crawler_repository.crawl.assert_called_once_with(url)
        redis_cache.set_to_redis.assert_called_once()
        assert result == crawled_results

    @pytest.mark.asyncio
    async def crawl_OK_cached_results_available_test(self):
        logger = Mock()
        redis_cache = Mock()
        crawler_repository = Mock()
        crawler_client = Mock()

        url = 'www.someurl.com'
        crawled_results = 'some results'

        redis_cache.get_from_redis = Mock(return_value=json.dumps(crawled_results))
        redis_cache.set_to_redis = Mock()
        crawler_repository.crawl = CoroutineMock()

        crawler_action = CrawlerAction(logger, config, redis_cache, crawler_repository, crawler_client)

        result = await crawler_action.crawl(url)

        redis_cache.get_from_redis.assert_called_once()
        crawler_repository.crawl.assert_not_called()
        redis_cache.set_to_redis.assert_not_called()
        assert result == crawled_results
