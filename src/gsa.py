import requests
import sys
from bs4 import BeautifulSoup
# from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from logger.config import logger
from database.select import next_sitemap_url
from database.insert import record_new_urls, create_new_crawl
from database.update import update_sitemap_status


def fetch_url(url):
    sys.setrecursionlimit(10000)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL: {url} - {str(e)}")
        return None

def parse_sitemap(sitemap_content):
    if not sitemap_content:
        return []

    soup = BeautifulSoup(sitemap_content, 'xml')
    urls = []

    for loc in soup.find_all('loc'):
        urls.append(loc.string)

    return urls


def crawl_sitemap(sitemap_url):
    sitemaps_to_crawl = [sitemap_url]
    visited_sitemaps = set()
    found_urls = []

    while sitemaps_to_crawl:
        current_sitemap = sitemaps_to_crawl.pop()
        if current_sitemap not in visited_sitemaps:
            visited_sitemaps.add(current_sitemap)
            sitemap_content = fetch_url(current_sitemap)
            urls = parse_sitemap(sitemap_content)

            for url in urls:
                if url.endswith('.xml') and url not in visited_sitemaps:
                    sitemaps_to_crawl.append(url)
                else:
                    found_urls.append(url)

    return found_urls



def main(sitemap_url, sitemap_id, domain_id):
    # Create new Crawl
    crawl_type = 'sitemap'
    agent = 'gsa_soup'
    crawl_id = create_new_crawl(crawl_type, sitemap_id, agent, domain_id)
    # Get Started
    visited_sitemaps = []
    raw_urls = crawl_sitemap(sitemap_url)

   # with Pool() as p:
    #    sitemap_contents = p.map(fetch_url, raw_urls)
    with ThreadPoolExecutor() as executor:
        sitemap_contents = list(executor.map(fetch_url, raw_urls))

    parsed_urls = list(map(parse_sitemap, sitemap_contents))
    flattened_urls = [url for sublist in parsed_urls for url in sublist]

    url_records = []
    for discovered_url in flattened_urls:
        logger.debug(f'New URL: {discovered_url} ')

    url_records = [(discovered_url, sitemap_url, crawl_id, True, domain_id) for discovered_url in flattened_urls]
    record_new_urls(url_records)
    # logger.debug(f'{len(url_records)} URLs added.')

    logger.debug(f'Sitemap {sitemap_id} Complete...')
    # Update the sitemap status
   # if update_sitemap_status(sitemap_id, crawl_id):
   #     logger.debug(f'Sitemap {sitemap_id} Complete...')
   # else:
   #     logger.error(f'Sitemap {sitemap_id} not marked complete...')



if __name__ == '__main__':
   while True:
       sitemap_url, sitemap_id, domain_id = next_sitemap_url()

       if not sitemap_url:
           break

       main(sitemap_url, sitemap_id, domain_id)

