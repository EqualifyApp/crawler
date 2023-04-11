import os

API_KEY = os.environ.get("API_KEY", "CrawlTheWorld")

def validate_api_key(api_key):
    """
    Authenticates the API key against the stored API key.

    Args:
        api_key (str): The API key to authenticate.

    Returns:
        tuple: A tuple containing a boolean indicating if the API key is valid and an error message if it's not.
    """
    if api_key == API_KEY:
        return True, None
    else:
        return False, "🛑 Invalid API Key! You Shall NOT PASS."
