import os
from flask import Flask, request, jsonify
# from utils.auth import validate_api_key
from logger.config import logger, configure_logger
from crawls.manager import spider_finder

# Let the world know we call ourselves the A11y🕸️!
app = Flask("A11y🕸️")

# Load the API key from the environment variable or set it to the default value
API_KEY = os.environ.get('API_KEY', 'CrawlTheWorld')

configure_logger()

@app.route('/crawl', methods=['POST'])
def crawl_handler():
    # Get the URL type parameter from the request
    url_type = request.args.get('type')

    # Get the JSON payload from the request
    payload = request.get_json()

    # Check the URL type and log a message accordingly
    if url_type == 'kraken':
        logger.info('🦑 Kraken Requested! YOU HAVE UNLEASHED ME!')
        response = spider_finder(payload)
        if response:
            return jsonify({"message": "Crawl started successfully"}), 200
        else:
            return jsonify({"error": "Crawl could not be started"}), 500
    elif url_type == 'harpoon':
        logger.info('🎯 Harpoon crawl requested')

    else:
        logger.warning('What do you want me to do? Invalid URL: %s', url_type)
        return jsonify({"error": "Invalid URL type"}), 400

    # Forward the request to the crawl module for handling
    # result = handle_crawl_request(payload)

    # Return the result
    # return result

if __name__ == '__main__':
    # Load the host and port from environment variables or set them to the default values
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 8084))

    logger.info('🚀 Starting the A11y🪵 Equalify Crawler...')
    app.run(host=HOST, port=PORT, debug=True)
