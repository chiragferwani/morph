"""
morph.scrapers.audio_scraper - Extract audio file URLs from a webpage.

This module fetches a webpage and finds all the audio resources on it,
including <audio> tags and <source> tags inside them.
"""

# 'requests' is used to fetch the webpage
import requests

# 'BeautifulSoup' is used to parse HTML and find audio tags
from bs4 import BeautifulSoup

# 'urljoin' converts relative URLs to full URLs
from urllib.parse import urljoin

# Import shared settings
from morph.core.config import DEFAULT_HEADERS, REQUEST_TIMEOUT, SUPPORTED_AUDIO_FORMATS

# Import the URL validator
from morph.utils.validator import validate_url


def scrape_audio(url, formats=None):
    """
    Scrape and extract all audio file URLs from a webpage.

    This function:
        1. Validates the URL
        2. Fetches the webpage HTML
        3. Finds all <audio> and <source> tags
        4. Also checks for direct links to audio files
        5. Returns a list of audio file URLs

    Parameters:
        url (str): The URL of the webpage to scrape.
        formats (list, optional): List of audio formats to include.
            Example: ['.mp3', '.wav']. If None, all supported formats are used.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the scraping succeeded.
            - 'url' (str): The URL that was scraped.
            - 'audio_files' (list): List of dicts with 'src' and 'filename'.
            - 'count' (int): Number of audio files found.
            - 'error' (str or None): Error message if scraping failed.
    """

    # ---- Step 1: Validate the URL ----
    if not validate_url(url):
        return {
            "success": False,
            "url": url,
            "audio_files": [],
            "count": 0,
            "error": "Invalid URL. Please provide a valid http:// or https:// URL.",
        }

    # Use all supported formats if none specified
    if formats is None:
        formats = SUPPORTED_AUDIO_FORMATS

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

        # We'll collect all found audio URLs here
        audio_files = []

        # ---- Step 4: Find audio in <audio> tags ----
        audio_from_tags = _find_audio_tags(soup, url)
        audio_files.extend(audio_from_tags)

        # ---- Step 5: Find audio in <a> (link) tags ----
        # Some pages link directly to audio files
        audio_from_links = _find_audio_links(soup, url, formats)
        audio_files.extend(audio_from_links)

        # ---- Step 6: Remove duplicates ----
        unique_audio = _remove_duplicates(audio_files)

        # ---- Step 7: Filter by format ----
        filtered_audio = _filter_by_format(unique_audio, formats)

        return {
            "success": True,
            "url": url,
            "audio_files": filtered_audio,
            "count": len(filtered_audio),
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "url": url,
            "audio_files": [],
            "count": 0,
            "error": f"Request timed out after {REQUEST_TIMEOUT} seconds.",
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "url": url,
            "audio_files": [],
            "count": 0,
            "error": "Could not connect to the website.",
        }

    except Exception as error:
        return {
            "success": False,
            "url": url,
            "audio_files": [],
            "count": 0,
            "error": f"Audio scraping failed: {str(error)}",
        }


def _find_audio_tags(soup, base_url):
    """
    Find audio files inside <audio> and <source> HTML tags.

    Parameters:
        soup (BeautifulSoup): The parsed HTML document.
        base_url (str): The page URL for resolving relative paths.

    Returns:
        list: List of dicts with 'src' and 'filename'.
    """
    found = []

    # Find all <audio> tags
    audio_tags = soup.find_all("audio")

    for audio_tag in audio_tags:
        # Check if the <audio> tag itself has a 'src' attribute
        src = audio_tag.get("src")
        if src:
            full_url = urljoin(base_url, src)
            filename = full_url.split("/")[-1].split("?")[0]
            found.append({"src": full_url, "filename": filename})

        # Also check for <source> tags inside the <audio> tag
        source_tags = audio_tag.find_all("source")
        for source_tag in source_tags:
            src = source_tag.get("src")
            if src:
                full_url = urljoin(base_url, src)
                filename = full_url.split("/")[-1].split("?")[0]
                found.append({"src": full_url, "filename": filename})

    return found


def _find_audio_links(soup, base_url, formats):
    """
    Find links (<a> tags) that point directly to audio files.

    Parameters:
        soup (BeautifulSoup): The parsed HTML document.
        base_url (str): The page URL for resolving relative paths.
        formats (list): List of audio format extensions to look for.

    Returns:
        list: List of dicts with 'src' and 'filename'.
    """
    found = []

    # Find all <a> (link) tags
    link_tags = soup.find_all("a", href=True)

    for link_tag in link_tags:
        href = link_tag["href"]

        # Check if the link points to an audio file
        lower_href = href.lower().split("?")[0]
        is_audio = False

        for fmt in formats:
            if lower_href.endswith(fmt):
                is_audio = True
                break

        if is_audio:
            full_url = urljoin(base_url, href)
            filename = full_url.split("/")[-1].split("?")[0]
            found.append({"src": full_url, "filename": filename})

    return found


def _remove_duplicates(audio_files):
    """
    Remove duplicate audio files based on their URL.

    Parameters:
        audio_files (list): List of audio info dictionaries.

    Returns:
        list: List with duplicates removed.
    """
    seen_urls = set()
    unique = []

    for audio in audio_files:
        if audio["src"] not in seen_urls:
            seen_urls.add(audio["src"])
            unique.append(audio)

    return unique


def _filter_by_format(audio_files, formats):
    """
    Filter audio files to only include files matching the given formats.

    Parameters:
        audio_files (list): List of audio info dictionaries.
        formats (list): List of format extensions like ['.mp3', '.wav'].

    Returns:
        list: Filtered list of audio files.
    """
    filtered = []

    for audio in audio_files:
        lower_src = audio["src"].lower().split("?")[0]

        for fmt in formats:
            if lower_src.endswith(fmt.lower()):
                filtered.append(audio)
                break

    return filtered
