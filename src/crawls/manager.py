import os
from logger.config import logger
from utils.check import should_sitemap_continue

# Crawl Types
from crawls.kraken import setup_kraken_cartocrawler, setup_kraken_spinnocracy


# Spider Router
# Which spider should call upon?
def spider_finder(payload):
    # Get the spider parameter from the payload
    spider_type = payload.get('spider')
# TODO break this out into crawl_type kraken|harpoon and then spider
    if spider_type == 'cartocrawler':
        response_message = 'CartoCrawler has been started!'
        logger.info(f' 🕷️ 🚀 CartoCrawler')
        return setup_kraken_cartocrawler()

    # Spinocracy
    # INFO Search for all URLs on a domain, not just the sitemap.
    elif spider_type == 'spinocracy':
        response_message = 'Spinocracy has started!'
        logger.info(f' 🕷️ 🚀 Spinnocracy')
        setup_kraken_spinnocracy()

    # No defined spider or other error
    else:
        # Return an error message if the kraken_type is invalid
        error_msg = {'error': 'Bad Spider. Check spider variable. '}
        logger.error(f' 🕷️ 💀 Spider selection failed. Check spider_type ')
        response = jsonify(error_msg)
        response.status_code = 400
        return response
