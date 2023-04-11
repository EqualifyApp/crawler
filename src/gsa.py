import sys
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from logger.config import logger
from database.select import next_sitemap_url
from database.insert import record_new_urls, create_new_crawl


def fetch_sitemap_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching sitemap URL: {url} - {str(e)}")
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
            sitemap_content = fetch_sitemap_content(current_sitemap)
            urls = parse_sitemap(sitemap_content)

            for url in urls:
                if url.endswith('.xml') and url not in visited_sitemaps:
                    sitemaps_to_crawl.append(url)
                else:
                    found_urls.append(url)

    return found_urls


def main(sitemap_url, sitemap_id, domain_id):
    crawl_type = 'sitemap'
    agent = 'gsa_soup'
    crawl_id = create_new_crawl(crawl_type, sitemap_id, agent, domain_id)

    raw_urls = crawl_sitemap(sitemap_url)

    url_records = [(url, sitemap_url, crawl_id, True, domain_id) for url in raw_urls]

    record_new_urls(url_records)
    logger.debug(f'{len(url_records)} URLs added.')

    logger.debug(f'Sitemap {sitemap_id} Complete...')


if __name__ == '__main__':
    while True:
        sitemap_url, sitemap_id, domain_id = next_sitemap_url()

        if not sitemap_url:
            break

        main(sitemap_url, sitemap_id, domain_id)
