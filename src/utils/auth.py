import os
from functools import wraps
from flask import request, abort
from .auth import authenticate

API_KEY = os.environ.get("API_KEY", "CrawlTheWorld")

def authenticate(api_key):
    """
    Authenticates the API key against the provided API key.

    Args:
        api_key (str): The API key to authenticate.

    Returns:
        tuple: A tuple containing a boolean indicating if the API key is valid and an error message if it's not.
    """
    # Check if the provided API key matches the stored API key
    if api_key == API_KEY:
        # If the API key is valid, return a tuple with True and None for the error message
        return True, None
    else:
        # If the API key is invalid, return a tuple with False and an error message
        return False, "🛑 Invalid API Key! You Shall NOT PASS."

def requires_auth(api_key):
    """
    Decorator that checks if the request is authenticated.

    Args:
        api_key (str): The API key to authenticate.

    Returns:
        function: The decorated function.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the authorization header from the request
            auth = request.authorization
            # Authenticate the API key using the authenticate() function
            if not auth or not authenticate(auth.username)[0]:
                # If the authentication fails, return a 401 Unauthorized HTTP status code and the error message
                abort(401, authenticate(auth.username)[1])
            # If the authentication succeeds, execute the decorated function
            return f(*args, **kwargs)
        # Return the decorated function
        return decorated_function
    # Return the decorator function
    return decorator
