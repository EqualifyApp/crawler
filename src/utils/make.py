import uuid
from config import BOT_ID, DEFAULT_SPIDEY_SENSES
from database.select import get_useragent
import random

def new_uuid():
    """
    Generates a new UUID.

    Returns:
        str: A string representation of the UUID.
    """
    return str(uuid.uuid4())



def get_headers(spider):
    # Get Global Bot Settings
    bot_name = BOT_ID['name']
    bot_version = BOT_ID['version']
    bot_url = BOT_ID['url']
    bot_description = BOT_ID['description']

    # Get User Agent
    user_agent, user_agent_id = get_useragent()

    # Set Headers
    headers = {
        'User-Agent': f'{user_agent} {bot_name}|{spider}/{bot_version} ({bot_url}) {bot_description}',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': f'{bot_url}'
    }

    return headers, user_agent_id

def get_spidey_senses(spider):
    # Get the default settings
    settings = DEFAULT_SPIDEY_SENSES.copy()

    # Check if the spider has its own settings
    if hasattr(spider, 'spidey_senses'):
        spidey_senses = spider.spidey_senses
        settings.update(spidey_senses)

    return settings