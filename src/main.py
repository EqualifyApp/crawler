import os
from logger.config import logger
from crawls.kraken import setup_kraken_cartocrawler

logger.info('🏠 Starting 🚀 the A11y🪵  Equalify Crawler...')
setup_kraken_cartocrawler()
