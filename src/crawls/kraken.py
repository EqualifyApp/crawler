import json
import subprocess
from logger.config import logger
from flask import jsonify
from database.select import next_sitemap_url
from database.update import update_crawl_status
from database.insert import record_new_crawl
from utils.make import new_uuid
from utils.check import is_url_sitemap
from crawls.spiders import start_cartocrawler

This script takes the json body payload of 'spider' and executes the approperiate function



def spider_finder(payload):


    # Get the spider parameter from the payload
    spider_type = payload.get('spider')

    if spider_type == 'cartocrawler':
        response_message = 'CartoCrawler has been started!'
        logger.info(f' 🕷️ 🚀 CartoCrawler')
        launch_cartocrawler()

    # Spinocracy
    # INFO Search for all URLs on a domain, not just the sitemap.
    elif spider_type == 'spinocracy':
        response_message = 'Spinocracy has started!'
        logger.info(f' 🕷️ 🚀 Spinnocracy')
        launch_spinocracy()

    # No defined spider or other error
    else:
        # Return an error message if the kraken_type is invalid
        error_msg = {'error': 'Bad Spider. Check spider variable. '}
        logger.error(f' 🕷️ 💀 Spider selection failed. Check spider_type ')
        response = jsonify(error_msg)
        response.status_code = 400
        return response


def setup_cartocrawler():
    sitemap, domain_id = next_sitemap_url()
    crawl_uuid = new_uuid()
    actor_id = 'cartocrawler'
    started_by = 'request'
    crawl_type = 'kraken'
    start_url = sitemap
    crawl_create_status = record_new_crawl(actor_id, started_by, crawl_uuid, crawl_type, domain_id, start_url)

    # Crawl Create Error
    if not crawl_create_status:
        logger.error('Cartocrawler unable to launch. Check launch_cartocrawler')

    # Crawl Created Successfully
    elif crawl_create_status:
        logger.info('New Crawl Created, Checking Sitemap')
        if is_url_sitemap(sitemap):
            start_cartocrawler(crawl_uuid, start_url)
            logger.info(f'Sitemap is good. Letting CartoCrawler know...')
        else:
            logger.info(f'{sitemap} is not a sitemap. Set up a loop?')

    # Other Error Logged
    else:
        logger.error('CartoCrawler Failure. See launch_cartocrawler')






