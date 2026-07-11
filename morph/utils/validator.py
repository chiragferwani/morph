"""
morph.utils.validator - Functions for validating URLs and checking connections.

This module provides simple helper functions to check if a URL is valid
and if the target website is reachable before attempting to scrape it.
"""

# We use 'urllib.parse' to break apart and check URLs
from urllib.parse import urlparse

# We use 'requests' to make HTTP requests and check if a website is reachable
import requests

# Import our timeout setting from the config
from morph.core.config import REQUEST_TIMEOUT, DEFAULT_HEADERS


def validate_url(url):
    """
    Check if the given URL is a valid web address.

    A valid URL must have:
        - A scheme (like 'http' or 'https')
        - A network location (like 'www.example.com')

    Parameters:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        # Parse the URL into its components (scheme, netloc, path, etc.)
        parsed = urlparse(url)

        # Check that both scheme and netloc exist
        # scheme = 'http' or 'https'
        # netloc = 'www.example.com'
        has_scheme = parsed.scheme in ["http", "https"]
        has_netloc = len(parsed.netloc) > 0

        # URL is valid only if both parts are present
        return has_scheme and has_netloc

    except Exception:
        # If parsing fails for any reason, the URL is not valid
        return False


def check_connection(url):
    """
    Check if we can actually reach the website at the given URL.

    This sends a HEAD request (which is faster than GET because
    it doesn't download the full page content).

    Parameters:
        url (str): The URL to check.

    Returns:
        dict: A dictionary with two keys:
            - 'reachable' (bool): True if the site responded successfully.
            - 'status_code' (int or None): The HTTP status code, or None if unreachable.
            - 'error' (str or None): Error message if something went wrong.
    """
    # First, make sure the URL itself is valid
    if not validate_url(url):
        return {
            "reachable": False,
            "status_code": None,
            "error": "Invalid URL format. Please use http:// or https://",
        }

    try:
        # Send a HEAD request to the URL (faster than GET)
        response = requests.head(
            url,
            headers=DEFAULT_HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        # Check if the status code means success (200-299 range)
        is_successful = response.status_code >= 200 and response.status_code < 300

        return {
            "reachable": is_successful,
            "status_code": response.status_code,
            "error": None if is_successful else f"Server returned status {response.status_code}",
        }

    except requests.exceptions.Timeout:
        # The server took too long to respond
        return {
            "reachable": False,
            "status_code": None,
            "error": f"Connection timed out after {REQUEST_TIMEOUT} seconds.",
        }

    except requests.exceptions.ConnectionError:
        # Could not connect to the server at all
        return {
            "reachable": False,
            "status_code": None,
            "error": "Could not connect to the server. Check your internet or the URL.",
        }

    except requests.exceptions.RequestException as error:
        # Catch any other request-related errors
        return {
            "reachable": False,
            "status_code": None,
            "error": f"Request failed: {str(error)}",
        }
