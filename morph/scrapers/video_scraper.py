"""
morph.scrapers.video_scraper - Extract video file URLs from a webpage.

This module fetches a webpage and finds all the video resources on it,
including <video> tags, <source> tags inside them, and direct links.
"""

# 'requests' is used to fetch the webpage
import requests

# 'BeautifulSoup' is used to parse HTML and find video tags
from bs4 import BeautifulSoup

# 'urljoin' converts relative URLs to full URLs
from urllib.parse import urljoin

# Import shared settings
from morph.core.config import DEFAULT_HEADERS, REQUEST_TIMEOUT, SUPPORTED_VIDEO_FORMATS

# Import the URL validator
from morph.utils.validator import validate_url


def scrape_video(url, formats=None):
    """
    Scrape and extract all video file URLs from a webpage.

    This function:
        1. Validates the URL
        2. Fetches the webpage HTML
        3. Finds all <video> and <source> tags
        4. Also checks for direct links to video files
        5. Returns a list of video file URLs

    Parameters:
        url (str): The URL of the webpage to scrape.
        formats (list, optional): List of video formats to include.
            Example: ['.mp4', '.webm']. If None, all supported formats are used.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the scraping succeeded.
            - 'url' (str): The URL that was scraped.
            - 'video_files' (list): List of dicts with 'src' and 'filename'.
            - 'count' (int): Number of video files found.
            - 'error' (str or None): Error message if scraping failed.
    """

    # ---- Step 1: Validate the URL ----
    if not validate_url(url):
        return {
            "success": False,
            "url": url,
            "video_files": [],
            "count": 0,
            "error": "Invalid URL. Please provide a valid http:// or https:// URL.",
        }

    # Use all supported formats if none specified
    if formats is None:
        formats = SUPPORTED_VIDEO_FORMATS

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

        # We'll collect all found video URLs here
        video_files = []

        # ---- Step 4: Find videos in <video> tags ----
        videos_from_tags = _find_video_tags(soup, url)
        video_files.extend(videos_from_tags)

        # ---- Step 5: Find videos in <a> (link) tags ----
        videos_from_links = _find_video_links(soup, url, formats)
        video_files.extend(videos_from_links)

        # ---- Step 6: Remove duplicates ----
        unique_videos = _remove_duplicates(video_files)

        # ---- Step 7: Filter by format ----
        filtered_videos = _filter_by_format(unique_videos, formats)

        return {
            "success": True,
            "url": url,
            "video_files": filtered_videos,
            "count": len(filtered_videos),
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "url": url,
            "video_files": [],
            "count": 0,
            "error": f"Request timed out after {REQUEST_TIMEOUT} seconds.",
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "url": url,
            "video_files": [],
            "count": 0,
            "error": "Could not connect to the website.",
        }

    except Exception as error:
        return {
            "success": False,
            "url": url,
            "video_files": [],
            "count": 0,
            "error": f"Video scraping failed: {str(error)}",
        }


def _find_video_tags(soup, base_url):
    """
    Find video files inside <video> and <source> HTML tags.

    Parameters:
        soup (BeautifulSoup): The parsed HTML document.
        base_url (str): The page URL for resolving relative paths.

    Returns:
        list: List of dicts with 'src' and 'filename'.
    """
    found = []

    # Find all <video> tags
    video_tags = soup.find_all("video")

    for video_tag in video_tags:
        # Check if the <video> tag itself has a 'src' attribute
        src = video_tag.get("src")
        if src:
            full_url = urljoin(base_url, src)
            filename = full_url.split("/")[-1].split("?")[0]
            found.append({"src": full_url, "filename": filename})

        # Also check for <source> tags inside the <video> tag
        source_tags = video_tag.find_all("source")
        for source_tag in source_tags:
            src = source_tag.get("src")
            if src:
                full_url = urljoin(base_url, src)
                filename = full_url.split("/")[-1].split("?")[0]
                found.append({"src": full_url, "filename": filename})

    return found


def _find_video_links(soup, base_url, formats):
    """
    Find links (<a> tags) that point directly to video files.

    Parameters:
        soup (BeautifulSoup): The parsed HTML document.
        base_url (str): The page URL for resolving relative paths.
        formats (list): List of video format extensions to look for.

    Returns:
        list: List of dicts with 'src' and 'filename'.
    """
    found = []

    # Find all <a> (link) tags
    link_tags = soup.find_all("a", href=True)

    for link_tag in link_tags:
        href = link_tag["href"]

        # Check if the link points to a video file
        lower_href = href.lower().split("?")[0]
        is_video = False

        for fmt in formats:
            if lower_href.endswith(fmt):
                is_video = True
                break

        if is_video:
            full_url = urljoin(base_url, href)
            filename = full_url.split("/")[-1].split("?")[0]
            found.append({"src": full_url, "filename": filename})

    return found


def _remove_duplicates(video_files):
    """
    Remove duplicate video files based on their URL.

    Parameters:
        video_files (list): List of video info dictionaries.

    Returns:
        list: List with duplicates removed.
    """
    seen_urls = set()
    unique = []

    for video in video_files:
        if video["src"] not in seen_urls:
            seen_urls.add(video["src"])
            unique.append(video)

    return unique


def _filter_by_format(video_files, formats):
    """
    Filter video files to only include files matching the given formats.

    Parameters:
        video_files (list): List of video info dictionaries.
        formats (list): List of format extensions like ['.mp4', '.webm'].

    Returns:
        list: Filtered list of video files.
    """
    filtered = []

    for video in video_files:
        lower_src = video["src"].lower().split("?")[0]

        for fmt in formats:
            if lower_src.endswith(fmt.lower()):
                filtered.append(video)
                break

    return filtered
