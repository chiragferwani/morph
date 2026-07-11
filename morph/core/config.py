"""
morph.core.config - Configuration constants for the morph package.

This file holds all the settings used throughout the package.
Change values here to adjust behavior globally.
"""

# ---- HTTP Request Settings ----

# How long to wait (in seconds) before giving up on a web request
REQUEST_TIMEOUT = 30

# User-Agent header to send with requests (some sites block requests without one)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Headers sent with every HTTP request
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ---- Supported File Formats ----

# Image formats we look for when scraping
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"]

# Audio formats we look for when scraping
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".ogg", ".flac", ".aac"]

# Video formats we look for when scraping
SUPPORTED_VIDEO_FORMATS = [".mp4", ".mov", ".webm", ".avi", ".mkv"]

# ---- Export Settings ----

# Text formats available for exporting scraped data
EXPORT_TEXT_FORMATS = ["txt", "csv", "json"]

# ---- Download Settings ----

# Size of chunks (in bytes) when downloading files
# Smaller = less memory, larger = faster download
DOWNLOAD_CHUNK_SIZE = 8192

# Default folder name for saving downloaded files
DEFAULT_DOWNLOAD_DIR = "morph_downloads"

# ---- Video Processing Settings ----

# How often (in seconds) to capture a frame when extracting images from video
FRAME_CAPTURE_INTERVAL = 1.0

# ---- Web Interface Settings ----

# Default port for the Flask web server
WEB_SERVER_PORT = 5000

# Enable or disable debug mode for the web server
WEB_DEBUG_MODE = False
