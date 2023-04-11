import os
import importlib
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import SitemapSpider
# Database Operations
from database.insert import record_crawled_url
from database.update import update_crawl_status, update_crawl_user_agent, update_crawl_complete
# Utils & Configs
from utils.make import get_headers, get_spidey_senses
from logger.config import logger
from scrapy.utils.project import get_project_settings


# Log Emoji: 🕸️🕷️🗺️

class CartoCrawler(SitemapSpider):
    name = "carto"

    def __init__(self, *args, start_url=None, crawl_uuid=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_url = start_url
        self.crawl_uuid = crawl_uuid

        logger.debug(f'🕸️🕷️🗺️ Initializing CartoCrawler instance')

        # Get Headers
        # spider = 'cartocrawler'
        # headers, user_agent_id = get_headers(spider)
        # logger.debug(f'🕸️🕷️🗺️ {spider} headers set')

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
        self.spider_settings = spidey_senses
        logger.debug(f'🕸️🕷️🗺️ {spider} senses defined')

        # Add User Agent to Crawl Info
        if update_crawl_user_agent(user_agent_id, crawl_uuid):
            logger.debug(f'🕸️🕷️🗺️ Crawl {crawl_uuid} User Agent Recorded')
        else:
            logger.error(f'🕸️🕷️🗺️ Crawl {crawl_uuid} Failed to Record')

    def parse(self, response):
        # Log Found URL
        logger.debug(f'🕸️🕷️🗺️ Found URL: {response.url}')

        # Set variables for recording crawled url
        url = response.url
        crawl_uuid = self.crawl_uuid
        source_url = response.request.headers.get('Referer', None)

        # Record crawled URL
        record_crawled_url(url, crawl_uuid, source_url)
        logger.debug(f'🕸️🕷️🗺️ URL {response.url} added to crawled urls')

    def closed(self, reason):

        # Sitemap Complete
        if update_crawl_complete(self.crawl_uuid):
            logger.debug(f'🕸️🕷️🗺️ Crawl {self.crawl_uuid} successfully completed')
        else:
            logger.error(f'🕸️🕷️🗺️ Crawl {self.crawl_uuid} NOT RECORDED')

        logger.warning(f'CLOSING NOW')
        super().closed(reason)

def start_cartocrawler(start_url, crawl_uuid):
    # Get headers and user agent ID
    headers, user_agent_id = get_headers('cartocrawler')

    # Get the domain ID and record a new crawl in the database
    sitemap, domain_id = next_sitemap_url()
    crawl_create_status = record_new_crawl(2, 'request', crawl_uuid, 'kraken', domain_id, start_url)

    if not crawl_create_status:
        logger.error(f'🕸️🦑 Cartocrawler unable to launch. Check with the Kraken')
        return False

    # Start the crawler
    process = CrawlerProcess(get_project_settings())
    process.crawl(CartoCrawler, start_url=start_url, crawl_uuid=crawl_uuid, headers=headers)
    process.start()

 #   # Sitemap complete
 #   if update_crawl_complete(crawl_uuid):
 #       logger.debug(f'🕸️🕷️🗺️ Crawl {crawl_uuid} successfully recorded')
 #   else:
 #       logger.error(f'🕸️🕷️🗺️ Crawl {crawl_uuid} NOT RECORDED')

  #  return True
