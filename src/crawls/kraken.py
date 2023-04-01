import os
import threading
from logger.config import logger
from database.select import next_sitemap_url
from utils.make import new_uuid
from database.insert import record_new_crawl
from utils.check import is_url_sitemap
from crawls.spiders.cartocrawler import CartoCrawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider_in_thread(start_url):
    process = CrawlerProcess(get_project_settings())
    process.crawl(CartoCrawler, start_url=start_url)
    process.start(stop_after_crawl=True)  # This is the correct place for the parameter

def setup_kraken_cartocrawler():
    sitemap, domain_id = next_sitemap_url()
    crawl_uuid = new_uuid()
    logger.debug(f'New UUID Generated: {crawl_uuid} ')
    actor_id = 2
    started_by = 'request'
    crawl_type = 'kraken'
    start_url = sitemap
    crawl_create_status = record_new_crawl(actor_id, started_by, crawl_uuid, crawl_type, domain_id, start_url)

    # Crawl Create Error
    if not crawl_create_status:
        logger.error('🦑 Cartocrawler unable to launch. Check with the Kraken')
        return False
    # Crawl Created Successfully
    elif crawl_create_status:
        logger.info('🦑 New Crawl Created, Checking Sitemap')
        if is_url_sitemap(sitemap):
            logger.info(f'🦑 Sitemap is good. Letting CartoCrawler know...')
            t = threading.Thread(target=run_spider_in_thread, args=(start_url,))
            t.start()
        else:
            logger.info(f'{sitemap} is not a sitemap. Set up a loop?')

    # Other Error Logged
    else:
        logger.error('🦑 CartoCrawler Failure. Check with the Kraken')



def setup_kraken_spinnocracy():
    logger.error('🦑 Help me Jim! I\'m lost in the Kraken!  ')


