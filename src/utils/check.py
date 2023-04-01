from scrapy.utils.sitemap import is_sitemap
from logger.config import logger
from database.select import execute_select, select_pending_sitemap_count



def is_url_sitemap(url):
    try:
        if is_sitemap(url):
            logger.info(f'{url} is a sitemap url')
            return True
        else:
            logger.error(f'{url} is not a sitemap url')
            return False
    except Exception as e:
        logger.error(f'{url} check failed with error: {str(e)}')
        return False


def should_sitemap_continue():
    count = select_pending_sitemap_count()
    if count > 0:
        return True
    else:
        return False