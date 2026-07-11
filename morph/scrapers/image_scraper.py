"""
morph.scrapers.image_scraper - Extract image URLs from a webpage.

This module fetches a webpage and finds all the images on it,
returning their URLs so they can be previewed or downloaded.
"""

# 'requests' is used to fetch the webpage
import requests

# 'BeautifulSoup' is used to parse HTML and find image tags
from bs4 import BeautifulSoup

# 'urljoin' converts relative URLs (like "/images/photo.jpg") into
# full URLs (like "https://example.com/images/photo.jpg")
from urllib.parse import urljoin

# Import our shared settings
from morph.core.config import DEFAULT_HEADERS, REQUEST_TIMEOUT, SUPPORTED_IMAGE_FORMATS

# Import the URL validator
from morph.utils.validator import validate_url


def scrape_images(url, formats=None):
    """
    Scrape and extract all image URLs from a webpage.

    This function:
        1. Validates the URL
        2. Fetches the webpage HTML
        3. Finds all <img> tags
        4. Extracts the 'src' attribute from each image
        5. Converts relative URLs to absolute URLs
        6. Optionally filters by image format

    Parameters:
        url (str): The URL of the webpage to scrape.
        formats (list, optional): List of image formats to include.
            Example: ['.jpg', '.png']. If None, all images are included.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the scraping succeeded.
            - 'url' (str): The URL that was scraped.
            - 'images' (list): List of dicts, each with 'src', 'alt', 'filename'.
            - 'count' (int): Number of images found.
            - 'error' (str or None): Error message if scraping failed.
    """

    # ---- Step 1: Validate the URL ----
    if not validate_url(url):
        return {
            "success": False,
            "url": url,
            "images": [],
            "count": 0,
            "error": "Invalid URL. Please provide a valid http:// or https:// URL.",
        }

    try:
        # ---- Step 2: Fetch the webpage ----
        response = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        # ---- Step 3: Parse the HTML ----
        soup = BeautifulSoup(response.text, "html.parser")

        # ---- Step 4: Find all <img> tags ----
        img_tags = soup.find_all("img")

        # ---- Step 5: Extract image information ----
        images = []
        for img_tag in img_tags:
            # Get the image source URL
            image_info = _extract_image_info(img_tag, url)

            # Skip if no valid source was found
            if image_info is None:
                continue

            # Filter by format if specified
            if formats is not None:
                if not _matches_format(image_info["src"], formats):
                    continue

            images.append(image_info)

        # ---- Step 6: Remove duplicates ----
        unique_images = _remove_duplicate_images(images)

        return {
            "success": True,
            "url": url,
            "images": unique_images,
            "count": len(unique_images),
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "url": url,
            "images": [],
            "count": 0,
            "error": f"Request timed out after {REQUEST_TIMEOUT} seconds.",
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "url": url,
            "images": [],
            "count": 0,
            "error": "Could not connect to the website.",
        }

    except Exception as error:
        return {
            "success": False,
            "url": url,
            "images": [],
            "count": 0,
            "error": f"Image scraping failed: {str(error)}",
        }


def _extract_image_info(img_tag, base_url):
    """
    Extract image information from an <img> HTML tag.

    Parameters:
        img_tag: A BeautifulSoup <img> tag element.
        base_url (str): The base URL of the page (for resolving relative URLs).

    Returns:
        dict or None: Dictionary with 'src', 'alt', 'filename', or None if no source.
    """
    # Try to get the 'src' attribute (the image URL)
    src = img_tag.get("src")

    # Some images use 'data-src' for lazy loading
    if not src:
        src = img_tag.get("data-src")

    # If still no source found, skip this image
    if not src:
        return None

    # Skip data URIs (embedded base64 images) — they're not real URLs
    if src.startswith("data:"):
        return None

    # Convert relative URL to absolute URL
    # Example: "/images/photo.jpg" -> "https://example.com/images/photo.jpg"
    full_url = urljoin(base_url, src)

    # Get the alt text (image description), default to empty string
    alt_text = img_tag.get("alt", "")

    # Extract the filename from the URL
    filename = full_url.split("/")[-1].split("?")[0]

    return {
        "src": full_url,
        "alt": alt_text,
        "filename": filename,
    }


def _matches_format(image_url, formats):
    """
    Check if an image URL ends with one of the given formats.

    Parameters:
        image_url (str): The image URL to check.
        formats (list): List of format extensions like ['.jpg', '.png'].

    Returns:
        bool: True if the URL matches one of the formats.
    """
    # Convert the URL to lowercase for case-insensitive matching
    lower_url = image_url.lower().split("?")[0]

    # Check each format
    for fmt in formats:
        if lower_url.endswith(fmt.lower()):
            return True

    return False


def _remove_duplicate_images(images):
    """
    Remove duplicate images based on their source URL.

    Parameters:
        images (list): List of image info dictionaries.

    Returns:
        list: List with duplicates removed.
    """
    seen_urls = set()
    unique_images = []

    for image in images:
        # Only add if we haven't seen this URL before
        if image["src"] not in seen_urls:
            seen_urls.add(image["src"])
            unique_images.append(image)

    return unique_images
