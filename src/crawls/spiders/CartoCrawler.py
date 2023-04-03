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
# Log Emoji: 🕸️🕷️🗺️

def start_cartocrawler(crawl_uuid, start_url):
    carto_crawler = CartoCrawler(start_url=start_url, crawl_uuid=crawl_uuid)

    logger.debug(f'🕸️🕷️🗺️ Initializing CartoCrawler instance')

    # Update Crawl Status to queued
    status = 'queued'
    update_crawl_status(status, crawl_uuid)
    logger.info(f'🕸️🕷️🗺️ Spinning up CartoCrawler... ')

    # Get Headers
    spider = 'cartocrawler'
    headers, user_agent_id = get_headers(spider)
    logger.info(f'🕸️🕷️🗺️ {spider} headers set')

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
    spidey_senses.update(get_spidey_senses(carto_crawler))
    carto_crawler.spider_settings = spidey_senses
    logger.info(f'🕸️🕷️🗺️ {spider} senses defined')

    # Add User Agent to Crawl Info
    if update_crawl_user_agent(user_agent_id, crawl_uuid):
        logger.info(f'🕸️🕷️🗺️ Crawl {crawl_uuid} User Agent Recorded')
    else:
        logger.error(f'🕸️🕷️🗺️ Crawl {crawl_uuid} Failed to Record')

    # Set the starting URLs to crawl
    carto_crawler.sitemap_urls = [start_url]
    logger.info(f'🕸️🕷️🗺️ Starting URL set to {start_url}')

    # Create a CrawlerProcess
    process = CrawlerProcess(settings={
        'USER_AGENT': headers['User-Agent'],
        **carto_crawler.spider_settings
    })

    logger.debug(f'🕸️🕷️🗺️ CrawlerProcess created')

    # Start the CrawlerProcess
    process.crawl(carto_crawler.__class__, start_url=start_url, crawl_uuid=crawl_uuid)
    logger.info(f'🕸️🕷️🗺️ Crawler process started for {start_url}')
    process.start()

    logger.debug(f'🕸️🕷️🗺️ CrawlerProcess completed')

    # Crawl is done, log the results
    logger.info(f'🕸️🕷️🗺️ {carto_crawler.total_urls} crawled, {carto_crawler.new_urls} new URLs found, {carto_crawler.updated_urls} URLs updated')

    # Set Vars for What's Next
    crawl_type = 'kraken'
    # Dynamically import the kraken_whats_next function to avoid circular imports
    kraken_module = importlib.import_module('crawls.kraken')
    kraken_whats_next_func = getattr(kraken_module, 'kraken_whats_next')
    kraken_whats_next_func(crawl_type)



class CartoCrawler(SitemapSpider):
    name = "carto"

    def __init__(self, *args, start_url=None, crawl_uuid=None, **kwargs):
        super(CartoCrawler, self).__init__(*args, **kwargs)
        self.start_url = start_url
        self.crawl_uuid = crawl_uuid
        self.total_urls = 0
        self.new_urls = 0
        self.updated_urls = 0

        logger.debug(f'🕸️🕷️🗺️ Initializing CartoCrawler instance') # Added Log

        # Sitemap Complete
        if update_crawl_complete(crawl_uuid, self.new_urls, self.updated_urls):
            logger.info(f'🕸️🕷️🗺️ Crawl {crawl_uuid} successfully recorded')
        else:
            logger.error(f'🕸️🕷️🗺️ Crawl {crawl_uuid} NOT RECORDED')



    def parse(self, response):
        # Log Found URL
        logger.debug(f'🕸️🕷️🗺️ Found URL: {response.url}')

        # Set variables for recording crawled url
        url = response.url
        crawl_uuid = self.crawl_uuid
        source_url = response.request.headers.get('Referer', None)

        # Record crawled URL
        action = record_crawled_url(response.url, self.crawl_uuid, response.request.url)

        if action == 'add':
            logger.info(f'🕸️🕷️🗺️ URL {response.url} added to crawled urls')
            self.new_urls += 1
        elif action == 'update':
            logger.info(f'🕸️🕷️🗺️ URL {response.url} already in crawled urls')
            self.updated_urls += 1
