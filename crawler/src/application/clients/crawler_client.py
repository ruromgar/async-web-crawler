import copy
import re

import aiohttp
import asyncio
from bs4 import BeautifulSoup


class CrawlerClient:
    def __init__(self, logger, config):
        self._logger = logger
        self._config = config

        self._session = aiohttp.ClientSession()
        self._max_requests = self._config.MAX_CONCURRENT_REQUESTS

    async def start_crawler(self, base_url):
        """Starts the crawling process, adding the urls to crawl to a set.
        The set is processed in batches of MAX_CONCURRENT_REQUESTS until no
        new urls need to be processed. For testing purposes there's a hard stop
        at 100 visited urls - that can be removed.
        During the crawling a page map is built, using the parent url as a guide.

        Parameters
        -------
        base_url
            URL to crawl

        Returns
        -------
        The page map
        """

        domain = self.extract_domain_from_url(base_url)
        if not domain:
            self._logger.info('The URL provided is not valid.')
            return None

        urls = {(None, base_url)}
        visited_urls = set()
        page_map = {base_url: {}}

        while urls != set():
            if len(visited_urls) > 100:  # Stopping the crawler for testing purposes
                return page_map

            urls_to_process = list(urls)[:self._max_requests]  # Max concurrent petitions
            futures = [asyncio.create_task(self.crawl(u, domain)) for u in urls_to_process]

            try:
                crawled_urls = await asyncio.gather(*futures)
                # Crawled urls will be a list of lists - flattening
                crawled_urls = [it for sublist in crawled_urls for it in sublist]
                urls = urls - set(urls_to_process)  # Cleaning up the urls yet to visit
            except Exception as err:
                self._logger.error(f"Error {err} gathering crawled urls.")
                crawled_urls = []

            urls.update([u for u in crawled_urls if u[1] not in visited_urls])

            for parent, url in urls_to_process:
                visited_urls.add(url)
                page_map = self.build_page_map(page_map, parent, url)

        return page_map

    async def crawl(self, item, domain):
        """Crawls the URL provided if it belongs to the domain.

        Parameters
        -------
        item
            contains the parent (unused) and the url to crawl
        domain
            to check if the url needs to be crawled

        Returns
        -------
        List of tuples with the links found during the crawling and their parent.
        """

        _, url = item

        if domain not in url:
            self._logger.info(f'Page {url} does not belong to the original domain.')
            return []

        try:
            self._logger.info(f"Crawling {url}")
            response = await self._session.get(url)
            result = await response.text()

            soup = BeautifulSoup(result, 'html.parser')
            all_urls = [(url, self.build_full_url(url, link.get('href'))) for link in soup.find_all('a')]
            return all_urls

        except Exception as err:
            self._logger.error(f'Failed to crawl: {url} because of {err}')
            return []

    def extract_domain_from_url(self, url):
        """Gets the domain from the url. That domain will then be used
        to avoid crawling external links.

        Parameters
        -------
        url

        Returns
        -------
        Whatever is contained within the 'http(s)://' and the dot '.'
        of the url. If that patter is not found, this method returns None.
        """

        m = re.search('https?://([A-Za-z_0-9.-]+).*', url)
        return m.group(1) if m else None

    def build_full_url(self, base_url, child_url):
        """Helper method to build the full url in cases such as a /submit
        or /news.

        Parameters
        -------
        base_url
        child_url
            incomplete url

        Returns
        -------
        Full url
        """

        return child_url if 'http' in child_url else f'{base_url}/{child_url}'

    def build_page_map(self, page_map, parent, url):
        """Helper method to build the page map. Adds the url to the current
        pagemap, using the parent as a guide. Uses recursion to avoid hardcoding
        the depth.

        Parameters
        -------
        page_map
            current pagemap
        parent
            url from which the current url was parsed
        url
            current url

        Returns
        -------
        Full tree representing the page map, including the current url
        """

        if parent is None:  # Edge case: first crawl
            return page_map

        for k, v in page_map.items():
            if k == parent:
                v[url] = {}
                return page_map
            # Recursion to build the whole tree
            page_map[k] = self.build_page_map(copy.deepcopy(v), parent, url)

        return page_map
