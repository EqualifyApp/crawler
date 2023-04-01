import requests
from logger.config import logger
from database.select import execute_select, select_pending_sitemap_count

def is_url_sitemap(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('Content-Type')
        if 'sitemap' in content_type or 'xml' in content_type:
            logger.info(f'{url} is a sitemap URL')
            return True
        else:
            logger.error(f'{url} is not a sitemap URL')
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
