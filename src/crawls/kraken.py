import os
# Scrapy Imports
import scrapy
from scrapy.utils.project import get_project_settings
# Database Operations
from database.select import next_sitemap_url
from database.insert import record_new_crawl
# Utilities
from utils.make import new_uuid
from utils.check import is_url_sitemap
from logger.config import logger
from crawls.spiders.cartocrawler import start_cartocrawler
from scrapy.crawler import CrawlerProcess

# Log Emoji: 🕸️🦑

def setup_kraken_cartocrawler():
    sitemap, domain_id = next_sitemap_url()
    crawl_uuid = new_uuid()
    logger.debug(f'🕸️🦑 New UUID Generated: {crawl_uuid} ')
    actor_id = 2
    started_by = 'request'
    crawl_type = 'kraken'
    start_url = sitemap
    crawl_create_status = record_new_crawl(actor_id, started_by, crawl_uuid, crawl_type, domain_id, start_url)

    # Crawl Create Error
    if not crawl_create_status:
        logger.error('🕸️🦑 Cartocrawler unable to launch. Check with the Kraken')
        return False
    # Crawl Created Successfully
    elif crawl_create_status:
        logger.info('🕸️🦑 New Crawl Created, Checking Sitemap')
        if is_url_sitemap(sitemap):
            logger.info(f'🕸️🦑 Sitemap is good. Letting CartoCrawler know...')
            site_url = start_url

            start_cartocrawler(start_url, crawl_uuid)
            logger.info(f'🕸️🦑 CartoCrawler started for {start_url}')
            return True
        else:
            logger.warning(f'🕸️🦑 {sitemap} is not a sitemap. Set up a loop?')

    # Other Error Logged
    else:
        logger.error('🕸️🦑 CartoCrawler Failure. Check with the Kraken')

def kraken_whats_next(crawl_type):
    spider = 'cartocrawler'
    logger.info(f'🕸️🦑 Determining whats next for the {crawl_type}\'s {spider}... ')
    if crawl_type == 'kraken':
        # What should the Kraken do
        logger.info(f'🕸️🦑 This looks to be a {crawl_type}\'s {spider} ')
        if should_sitemap_continue():
            logger.info('🕸️🦑 More sitemaps for the Kraken, lets go again!!! ')
            setup_kraken_cartocrawler()
        else:
            logger.info('🕸️🦑 No more sitemaps to crawl. Calling it a day... ')
    elif crawl_type == 'harpoon':
        logger.warning(f'🕸️🦑 Harpoon asking for help! See manager... ')
    # What to do if crawl_type doesn't match
    else:
        logger.error(f'🕸️🦑 I\'m lost. Help me! See my manager... ')


def setup_kraken_spinnocracy():
    logger.critical('🕸️🦑 Oh no! The Kraken Spinnocracy is down...')
