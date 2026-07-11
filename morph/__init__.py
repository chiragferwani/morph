"""
morph - A Python Multi-Modal Web Scraping Package

This package can scrape and extract multiple types of web content
from a given website URL including text, images, audio, and video.
It also provides conversion utilities (OCR, speech-to-text, video processing).

Usage:
    from morph import scrape_text, scrape_images
    text = scrape_text("https://example.com")
"""

# ---- Version information ----
__version__ = "0.1.3"
__author__ = "Chirag"

# ---- Import all scraper functions so users can do: from morph import scrape_text ----
from morph.scrapers.text_scraper import scrape_text
from morph.scrapers.image_scraper import scrape_images
from morph.scrapers.audio_scraper import scrape_audio
from morph.scrapers.video_scraper import scrape_video

# ---- Import all converter functions ----
from morph.converters.image_converter import image_to_text
from morph.converters.audio_converter import audio_to_text
from morph.converters.video_converter import video_to_audio, video_to_text, video_to_images

# ---- Import utility functions ----
from morph.utils.downloader import download_file
from morph.utils.exporter import export_to_txt, export_to_csv, export_to_json, export_to_zip
from morph.utils.validator import validate_url, check_connection
