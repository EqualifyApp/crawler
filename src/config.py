BOT_ID = {
    'name': 'A11yCrawler',
    'version': '2.1',
    'url': 'https://github.com/EqualifyApp/crawler',
    'description': 'The A11yCrawler is a spider system to collect urls for further testing. Contact us if I am a bad bot.',
}


SITEMAP_FREQUENCY = 3600
# Default Spider Settings
# You can override these in the spider file. if desired. If no value is set in the spider file, the defaults below are used.

DEFAULT_SPIDEY_SENSES = {
    "COOKIES_ENABLED": False,               # Disable cookies
    "CONCURRENT_ITEMS": 50,                 # Number of concurrent items (per response) to process
    "CONCURRENT_REQUESTS": 16,              # Maximum concurrent requests
    #"DEPTH_LIMIT": 3,                      # Max depth that will be crawled. 0 for no limit
    "DNSCACHE_ENABLED": True,               # Enable DNS in-memory cache
    "DNS_TIMEOUT": 60,                      # Timeout for processing DNS queries
    "HTTPCACHE_ENABLED": False,             # Enable or disable caching
    "CONCURRENT_REQUESTS_PER_DOMAIN": 16,   # Maximum concurrent requests per domain
    "ROBOTSTXT_OBEY": True,                 # Obey robots.txt rules
    "AUTOTHROTTLE_ENABLED": True,           # Enable AutoThrottle extension
    "AUTOTHROTTLE_START_DELAY": 5,          # Initial delay before AutoThrottle starts adjusting the delay
    "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,   # Target concurrency for AutoThrottle
    # Logging Settings
    "AUTOTHROTTLE_DEBUG": False,             # Debug logs on Autothrottle
    "LOG_LEVEL": "INFO",                   # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    #"LOG_FILE": "logs/crawl.log",          # Where to save logs
    "LOG_ENABLED": True                     # Enable logging
}




# Definition of Spider Settings:

# COOKIES_ENABLED: Whether to enable cookies (if enabled, stores cookies between requests)
# CONCURRENT_ITEMS: Number of concurrent items (per response) to process
# CONCURRENT_REQUESTS: Maximum concurrent requests
# DEPTH_LIMIT: Max depth that will be crawled. 0 for no limit
# DNSCACHE_ENABLED: Enable DNS in-memory cache
# DNS_TIMEOUT: Timeout for processing DNS queries
# HTTPCACHE_ENABLED: Enable or disable caching
# CONCURRENT_REQUESTS_PER_DOMAIN: Maximum concurrent requests per domain
# ROBOTSTXT_OBEY: Obey robots.txt rules
# AUTOTHROTTLE_ENABLED: Enable AutoThrottle extension
# AUTOTHROTTLE_START_DELAY: Initial delay before AutoThrottle starts adjusting the delay
# AUTOTHROTTLE_TARGET_CONCURRENCY: Target concurrency for AutoThrottle
# AUTOTHROTTLE_DEBUG: Debug logs on Autothrottle
# LOG_LEVEL: Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
# LOG_FILE: Where to save logs
# LOG_ENABLED: Enable logging



