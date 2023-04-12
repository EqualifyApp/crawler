import sys
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
from logger.config import logger
from database.select import next_rosevelt_url
from database.insert import record_new_crawled_htmls, create_new_crawl_html
from urllib.parse import urljoin, urlparse


def crawl_webpage(url_id, url, domain_id):
    # Create new crawl
    agent = "rosevelt"
    crawl_type = "html"
    crawl_id = create_new_crawl_html(crawl_type, url_id, agent)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching URL: {url} - {str(e)}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    new_urls = []

    for link in soup.find_all("a", href=True):
        found_url = link["href"]
        parsed_url = urlparse(found_url)
        if not parsed_url.scheme:  # Ignore if it's a relative URL
            found_url = urljoin(url, found_url)

        new_urls.append({
            "source_url_id": url_id,
            "url": found_url,
            "crawl_id": crawl_id
        })
    # Log the number of new URLs found
    logger.info(f"Found {len(new_urls)} new urls")

    # Record found urls with: record_new_crawled_urls(new_urls)
    record_new_crawled_htmls(new_urls)


def main():
    while True:
        next_url = next_rosevelt_url()
        if not next_url:
            break

        url_id, url, domain_id = next_url
        crawl_webpage(url_id, url, domain_id)


def run_rosevelt_main():
    # Run Rosevelt main
    main()


if __name__ == "__main__":
    num_processes = 10
    processes = []

    # Spawn multiple processes
    for i in range(num_processes):
        process = Process(target=run_rosevelt_main)
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()
