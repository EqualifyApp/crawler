import os
from flask import Flask, request
from utils.auth import requires_auth
from logger.config import logger

# Let the world know we call ourselves the A11y🕸️!
app = Flask("A11y🕸️")

# Load the API key from the environment variable or set it to the default value
API_KEY = os.environ.get('API_KEY', 'CrawlTheWorld')


@app.route('/crawl', methods=['POST'])
@requires_auth(API_KEY)
def crawl_handler():
    """
    Handle incoming crawl requests.

    This function is a Flask route handler that handles incoming HTTP POST requests to the "/crawl" endpoint. The route
    is protected by the `@requires_auth` decorator from `utils/auth.py`, which authenticates the request with an API key
    before allowing it to access this function.

    The function first extracts the "type" parameter from the request URL and logs a message indicating the type of crawl
    requested. It then extracts the JSON payload from the request and forwards it to the `handle_crawl_request()`
    function for handling.

    Returns:
        str: A JSON string containing the response data.
    """
    # Get the URL type parameter from the request
    type = request.args.get('type')

    # Check the URL type and log a message accordingly
    if type == 'kraken':
        logger.info('🦑 Kraken Requested! YOU HAVE UNLEASHED ME!')

    elif type == 'harpoon':
        logger.info('🎯 Harpoon crawl requested')

    else:
        logger.warning('What do you want me to do? Invalid URL: %s', url_type)

    # Get the JSON payload from the request
    payload = request.get_json()

    # Forward the request to the crawl module for handling
    result = handle_crawl_request(payload)

    # Return the result
    return result


def configure_logger():
    """
    Configures the logger for the application.

    This function sets up the logger named "A11y🪵" by configuring it to log messages to the console with a format of
    `%(asctime)s - %(name)s - [%(levelname)s] - %(message)s`. The logger is set to a level of `DEBUG` and has a console
    handler with a level of `INFO`. If the logger already has handlers, it will not be reconfigured.
    """
    # Use the logger from logging_config.py
    global logger
    logger = logging.getLogger("A11y🪵")


if __name__ == '__main__':
    # Load the host and port from environment variables or set them to the default values
    HOST = os.environ.get('HOST', 'localhost')
    PORT = int(os.environ.get('PORT', 8084))

    # Configure the logger
    configure_logger()

    # Start the Flask app
    logger.info('🚀 Starting the A11y🪵 Equalify Crawler...')
    app.run(host=HOST, port=PORT)
