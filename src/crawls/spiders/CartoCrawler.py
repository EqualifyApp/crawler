import os
import scrapy
from scrapy.spiders import SitemapSpider
# Database Operations
from database.insert import record_crawled_url
from database.update import update_crawl_status, update_crawl_user_agent, update_crawl_complete
# Utils & Configs
from utils.make import get_headers, get_spidey_senses
from logger.config import logger

class CartoCrawler(SitemapSpider):
    name = "CartoCrawler"
    """
    A Scrapy spider for crawling sitemaps.

    Attributes
    ----------
    total_urls : int
        Total number of URLs crawled
    new_urls : int
        Number of new URLs found
    updated_urls : int
        Number of URLs updated

    Methods
    -------
    start_cartocrawler(crawl_uuid, start_url)
        Starts the CartoCrawler with the given crawl UUID and start URL.
    parse(response)
        Parses the given response and records the crawled URL.

    """
    total_urls = 0
    new_urls = 0
    updated_urls = 0

    def start_cartocrawler(self, crawl_uuid, start_url):
        """
        Starts the CartoCrawler with the given crawl UUID and start URL.

        Parameters
        ----------
        crawl_uuid : str
            The UUID of the crawl
        start_url : str
            The URL of the sitemap to start crawling
        """
        # Update Crawl Status to queued
        status = 'queued'
        update_crawl_status(status, crawl_uuid)
        logger.info(f'Spinning up CartoCrawler... ')

        # Get Headers
        spider = 'cartocrawler'
        headers, user_agent_id = get_headers(spider)
        logger.info('CartoCrawler headers set')

        # Define spider-specific settings
        spidey_senses = {
            'CONCURRENT_REQUESTS': 8,
            'DNSCACHE_ENABLED': False,
            'SITEMAP_FOLLOW': True,
            'SITEMAP_ALTERNATIVE_LINKS': True,
            'ROBOTS_TXT': False,
            'ROBOTSTXT_OBEY': False,
            'PRIORITY': 1,
            'MAX_URLS': 10000,
        }
        spidey_senses.update(get_spidey_senses(self))
        self.spider_settings = spidey_senses
        logger.info(f'{spider} senses defined')

        # Add User Agent to Crawl Info

        if update_crawl_user_agent(user_agent_id, crawl_uuid):
            logger.info(f'Crawl {crawl_uuid} User Agent Recorded')
        else:
            logger.error(f'Crawl {crawl_uuid} Failed to Record')

        # Set the starting URLs to crawl
        self.sitemap_urls = [start_url]
        logger.info(f'Starting URL set to {start_url}')

        # Roll to Parser
        for url in self.sitemap_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

        # Crawl is done, log the results
        logger.info(f'{self.total_urls} crawled, {self.new_urls} new URLs found, {self.updated_urls} URLs updated')
    # Set Vars for What's Next
        spider = 'cartocrawler'
        crawl_type = 'kraken'
        kraken_whats_next(self, spider, crawl_type)
    # End of Script

        # Sitemap Complete
        if update_crawl_complete(crawl_uuid, self.new_urls, self.updated_urls):
            logger.info(f'Crawl {crawl_uuid} successfully recorded')
        else:
            logger.error(f'Crawl {crawl_uuid} NOT RECORDED')


    def parse(self, response):
        """
        Parses the given response and records the crawled URL.

        Parameters:
        -----------
        response : scrapy.Response
            The response to parse.

        Returns:
        --------
        None
        """
        # Log Found URL
        logger.debug(f'Found URL: {response.url}')

        # Set variables for recording crawled url
        url = response.url
        crawl_uuid = self.crawl_uuid
        source_url = response.request.headers.get('Referer', None)

        # Record crawled URL
        action = record_crawled_url(response.url, self.crawl_uuid, response.request.url)

        # Update counters
        if action == 'add':
            self.new_urls += 1
        elif action == 'update':
            self.updated_urls += 1

    def kraken_whats_next(self):
        spider = 'cartocrawler'
        crawl_type = 'kraken'
        logger.info(f'Determining whats next for the {crawl_type}\'s {spider}... ')
        if crawl_type == 'kraken':
            # What should the Kraken do
            logger.info(f'This looks to be a {crawl_type}\'s {spider} ')
            if should_sitemap_continue():
                logger.info('More sitemaps for the {crawl_type}, lets go again!!! ')
                setup_kraken_cartocrawler()
            else:
                logger.info('No more sitemaps to crawl. Calling it a day... ')
        elif crawl_type == 'harpoon':
            logger.warning(f'Harpoon asking for help! See manager... ')
        # What to do if crawl_type doesn't match
        else:
            logger.error(f'I\'m lost. Help me! See my manager... ')
