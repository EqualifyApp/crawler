import os
from flask import Flask, request, jsonify
from logger.config import logger, configure_logger
from crawls.kraken import setup_kraken_cartocrawler

app = Flask("A11y🕸️")

API_KEY = os.environ.get('API_KEY', 'CrawlTheWorld')

configure_logger()

@app.route('/crawl', methods=['POST'])
def crawl_handler():
    url_type = request.args.get('type')
    payload = request.get_json()

    if url_type == 'kraken':
        logger.info('🦑 Kraken Requested! YOU HAVE UNLEASHED ME!')
        crawl_started = setup_kraken_cartocrawler()  # Store result? Should we?

        if crawl_started:  # Check the result of the function call
            logger.info('🦑 Rolling!')
            return jsonify({"message": "Crawl started successfully"}), 200
        else:
            return jsonify({"error": "Crawl could not be started"}), 500
    elif url_type == 'harpoon':
        logger.info('🎯 Harpoon crawl requested')
    else:
        logger.warning('What do you want me to do? Invalid URL: %s', url_type)
        return jsonify({"error": "Invalid URL type"}), 400


if __name__ == '__main__':
    # Load the host and port from environment vars or set them to the default values
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 8084))

    logger.info('🚀 Starting the A11y🪵 Equalify Crawler...')
    app.run