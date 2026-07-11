"""
morph.scrapers.text_scraper - Extract visible text content from a webpage.

This module fetches a webpage and pulls out all the visible text,
removing scripts, styles, and HTML tags. It returns clean, readable text.
"""

# 'requests' is used to fetch the webpage content from the internet
import requests

# 'BeautifulSoup' is used to parse HTML and extract text from it
from bs4 import BeautifulSoup

# Import our shared settings
from morph.core.config import DEFAULT_HEADERS, REQUEST_TIMEOUT

# Import the URL validator to check URLs before scraping
from morph.utils.validator import validate_url


def scrape_text(url):
    """
    Scrape and extract all visible text from a webpage.

    This function:
        1. Validates the URL
        2. Fetches the webpage HTML
        3. Removes script and style tags
        4. Extracts all visible text
        5. Cleans up extra whitespace

    Parameters:
        url (str): The URL of the webpage to scrape.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the scraping succeeded.
            - 'url' (str): The URL that was scraped.
            - 'title' (str or None): The page title.
            - 'text' (str): The extracted text content.
            - 'word_count' (int): Number of words in the extracted text.
            - 'error' (str or None): Error message if scraping failed.
    """

    # ---- Step 1: Validate the URL ----
    if not validate_url(url):
        return {
            "success": False,
            "url": url,
            "title": None,
            "text": "",
            "word_count": 0,
            "error": "Invalid URL. Please provide a valid http:// or https:// URL.",
        }

    try:
        # ---- Step 2: Fetch the webpage ----
        # Send a GET request to download the page HTML
        response = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )

        # Raise an error if the server returned a bad status code (like 404 or 500)
        response.raise_for_status()

        # ---- Step 3: Parse the HTML ----
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # ---- Step 4: Get the page title ----
        page_title = _extract_title(soup)

        # ---- Step 5: Remove unwanted elements ----
        # Remove all <script> and <style> tags because they contain
        # code, not visible text
        _remove_unwanted_tags(soup)

        # ---- Step 6: Extract the visible text ----
        raw_text = soup.get_text()

        # ---- Step 7: Clean up the text ----
        clean_text = _clean_text(raw_text)

        # ---- Step 8: Count the words ----
        word_count = len(clean_text.split())

        return {
            "success": True,
            "url": url,
            "title": page_title,
            "text": clean_text,
            "word_count": word_count,
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "url": url,
            "title": None,
            "text": "",
            "word_count": 0,
            "error": f"Request timed out after {REQUEST_TIMEOUT} seconds.",
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "url": url,
            "title": None,
            "text": "",
            "word_count": 0,
            "error": "Could not connect to the website. Check your internet connection.",
        }

    except requests.exceptions.HTTPError as error:
        return {
            "success": False,
            "url": url,
            "title": None,
            "text": "",
            "word_count": 0,
            "error": f"HTTP error: {str(error)}",
        }

    except Exception as error:
        return {
            "success": False,
            "url": url,
            "title": None,
            "text": "",
            "word_count": 0,
            "error": f"Text scraping failed: {str(error)}",
        }


def _extract_title(soup):
    """
    Extract the title from a parsed HTML page.

    Parameters:
        soup (BeautifulSoup): The parsed HTML document.

    Returns:
        str or None: The page title, or None if no title found.
    """
    # Try to find the <title> tag
    title_tag = soup.find("title")

    # Return the title text if found, otherwise None
    if title_tag and title_tag.string:
        return title_tag.string.strip()
    return None


def _remove_unwanted_tags(soup):
    """
    Remove script, style, and other non-visible tags from the HTML.

    This modifies the soup object in place (does not return anything).

    Parameters:
        soup (BeautifulSoup): The parsed HTML document to clean.
    """
    # List of tag names that contain non-visible content
    tags_to_remove = ["script", "style", "noscript", "iframe", "svg"]

    # Find and remove each unwanted tag
    for tag_name in tags_to_remove:
        # Find all tags with this name
        found_tags = soup.find_all(tag_name)

        # Remove each one from the document
        for tag in found_tags:
            tag.decompose()


def _clean_text(raw_text):
    """
    Clean up raw text by removing extra whitespace and blank lines.

    Parameters:
        raw_text (str): The raw text with extra spaces and blank lines.

    Returns:
        str: Cleaned text with normalized whitespace.
    """
    # Split the text into individual lines
    lines = raw_text.splitlines()

    # Clean up each line by removing leading/trailing whitespace
    cleaned_lines = []
    for line in lines:
        stripped_line = line.strip()

        # Only keep lines that have some content
        if stripped_line:
            cleaned_lines.append(stripped_line)

    # Join the cleaned lines back together with newlines
    return "\n".join(cleaned_lines)
