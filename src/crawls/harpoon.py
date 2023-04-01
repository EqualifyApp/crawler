import json
from logger.config import logger
from flask import jsonify
from utils.sorter import is_url_sitemap

def harpoon_handler(payload):
    target = payload.get('domain', None) or payload.get('url', None)
    if not target:
        error_message = "Bad Request!🐶 Check your TARGET and resend, or don't..."
        response = jsonify({'status': 'error', 'message': error_message})
        response.status_code = 400
        return response
    # Check if target is a sitemap or not
    if is_url_sitemap(url):
        # URL is a sitemap
        if


    else:
        # URL is NOT a sitemap



        return is_sitemap(url)
        if is_sitemap is TRUE:
            if



    # Check if target is a sitemap or not with utils/sorter

    # Perform the targeted crawl
    results = throw_harpoon(target)


    #






    # Create the response object
    response = {'status': 'success', 'results': results}

    # Return the response as a JSON string
    return jsonify(response)











def harpoon_crawl(payload):
    """
    Handles a harpoon crawl request.

    This function takes a JSON payload containing the "target" parameter, which should be a URL or domain to crawl,
    and the "database" and "output" parameters, which control whether the results should be written to the database and
    output in the response, respectively.

    Returns:
        str: A JSON string containing the response data.
    """
    try:
        # Parse the payload JSON and extract the target parameter
        data = json.loads(payload)
        target = data["target"]

        # Check if the target is a valid URL or domain
        # Your validation logic here

        # Log a message indicating that the crawl is starting
        logger.info("Good Request. Let's roll")

        # Perform the crawl and generate the response
        # Your crawl logic here

        # Return the response
        # Your response generation logic here
    except (ValueError, KeyError):
        # If the payload is invalid or the target parameter is missing, log an error

        logger.error("Bad Request!🐶 Check your TARGET and resend, or don't...")
        # Return an error response
        # Your error response generation logic here





"""
Harpoon
This is for targeted crawls.

This function makes use of the below input

type=harpoon
Body
    target: string is required contains url or domain
    database: bool - decides if should write results to database or not. defaults to true
    output: bool    - decides if should output results vis response to request or not. defaults to false

I want to first check if the body, formatted in JSON, has a target that is either a domain or url. If it does, log.info:"Good Request. Lets Roll" if it is not a good url or domain, log.error:"Bad Request! [emoji for bad dog] Target invalid. Try again, or don't



"""