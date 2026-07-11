"""
morph.utils.downloader - Functions for downloading files from the internet.

This module provides a simple way to download any file (image, audio, video)
from a URL and save it to the local filesystem.
"""

import os

# 'requests' is used for making HTTP requests to download files
import requests

# Import settings from our config
from morph.core.config import (
    DEFAULT_HEADERS,
    REQUEST_TIMEOUT,
    DOWNLOAD_CHUNK_SIZE,
    DEFAULT_DOWNLOAD_DIR,
)


def download_file(url, save_path=None, save_dir=None):
    """
    Download a file from a URL and save it to disk.

    The file is downloaded in small chunks to avoid using too much memory,
    which is important for large files like videos.

    Parameters:
        url (str): The URL of the file to download.
        save_path (str, optional): Full path where the file should be saved.
            If not provided, the filename is extracted from the URL.
        save_dir (str, optional): Directory to save the file in.
            Defaults to 'morph_downloads' in the current directory.

    Returns:
        dict: A dictionary with:
            - 'success' (bool): Whether the download succeeded.
            - 'file_path' (str or None): Path to the saved file.
            - 'file_size' (int): Size of the downloaded file in bytes.
            - 'error' (str or None): Error message if download failed.
    """
    try:
        # ---- Step 1: Figure out where to save the file ----

        if save_path is None:
            # Extract the filename from the URL
            # For example: "https://example.com/images/photo.jpg" -> "photo.jpg"
            filename = _extract_filename_from_url(url)

            # Use the provided directory, or the default one
            if save_dir is None:
                save_dir = DEFAULT_DOWNLOAD_DIR

            # Create the directory if it doesn't exist yet
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Combine directory and filename to get the full path
            save_path = os.path.join(save_dir, filename)

        # ---- Step 2: Download the file in chunks ----

        # Use stream=True so we don't load the entire file into memory at once
        response = requests.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=REQUEST_TIMEOUT,
            stream=True,
        )

        # Raise an error if the server returned a bad status code
        response.raise_for_status()

        # Keep track of how many bytes we've downloaded
        total_bytes = 0

        # Open the file in binary write mode and save chunks
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                # Only write non-empty chunks
                if chunk:
                    file.write(chunk)
                    total_bytes = total_bytes + len(chunk)

        return {
            "success": True,
            "file_path": save_path,
            "file_size": total_bytes,
            "error": None,
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "file_path": None,
            "file_size": 0,
            "error": f"Download timed out after {REQUEST_TIMEOUT} seconds.",
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "file_path": None,
            "file_size": 0,
            "error": "Could not connect to the server to download the file.",
        }

    except PermissionError:
        return {
            "success": False,
            "file_path": None,
            "file_size": 0,
            "error": f"Permission denied: cannot write to '{save_path}'.",
        }

    except Exception as error:
        return {
            "success": False,
            "file_path": None,
            "file_size": 0,
            "error": f"Download failed: {str(error)}",
        }


def _extract_filename_from_url(url):
    """
    Extract a filename from a URL.

    For example:
        "https://example.com/images/photo.jpg?size=large"
        becomes "photo.jpg"

    If no filename can be found, returns a generic name.

    Parameters:
        url (str): The URL to extract the filename from.

    Returns:
        str: The extracted filename.
    """
    # Remove any query parameters (everything after '?')
    clean_url = url.split("?")[0]

    # Get the last part of the URL path
    filename = clean_url.split("/")[-1]

    # If no filename was found, use a generic name
    if not filename or "." not in filename:
        filename = "downloaded_file"

    return filename
