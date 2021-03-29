import re

from application.actions.crawler_action import CrawlerAction
from fastapi import FastAPI, HTTPException
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCornConfig


class CrawlerServer:
    _hypercorn_config = None
    _fastapi = FastAPI()

    def __init__(self, logger, config, crawler_action: CrawlerAction):
        self._hypercorn_config = HyperCornConfig()
        self._logger = logger
        self._config = config
        self._crawler_action = crawler_action

    async def run_server(self):
        """Starts the server with the config parameters.
        """

        self._hypercorn_config.bind = [f'0.0.0.0:{self._config.FASTAPI_CONFIG["port"]}']
        self._hypercorn_config.keep_alive_timeout = 90
        self.add_routes()
        await serve(self._fastapi, self._hypercorn_config)

    def add_routes(self):
        """Maps the endpoint routes with their methods.
        """

        self._fastapi.add_api_route(path="/_health", endpoint=self.healthcheck, methods=["GET"])
        self._fastapi.add_api_route(path="/api/crawl", endpoint=self.crawl, methods=["GET"])

    async def crawl(self, url: str):
        """Crawls the provided website. The regexp validation comes
        from the Django code: https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45

        Parameters
        -------
        url
            website to crawl

        Returns
        -------
        Crawling results if everything went right and None otherwise
        """

        # Adding this just because the exercise explicitly requires it
        if not url.startswith('http'):
            url = f'http://{url}'

        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if re.match(regex, url) is None:
            raise HTTPException(status_code=400, detail="Invalid URL")

        return await self._crawler_action.crawl(url)

    def healthcheck(self):
        """Simple healthcheck.
        """

        return {"status": 200}
