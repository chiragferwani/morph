"""
test_scrapers.py - Unit tests for the morph scraper modules.

These tests check that our scrapers work correctly with real websites.
Run with: python -m pytest tests/test_scrapers.py -v
"""

import unittest

# Import the scraper functions we want to test
from morph.scrapers.text_scraper import scrape_text
from morph.scrapers.image_scraper import scrape_images
from morph.scrapers.audio_scraper import scrape_audio
from morph.scrapers.video_scraper import scrape_video


class TestTextScraper(unittest.TestCase):
    """Tests for the text scraper module."""

    def test_scrape_text_valid_url(self):
        """Test that scraping a valid URL returns text successfully."""
        # Use example.com — it's a simple, reliable test page
        result = scrape_text("https://example.com")

        # Check that the scrape succeeded
        self.assertTrue(result["success"])

        # Check that some text was found
        self.assertGreater(len(result["text"]), 0)

        # Check that word count is positive
        self.assertGreater(result["word_count"], 0)

        # Check that no error was returned
        self.assertIsNone(result["error"])

    def test_scrape_text_invalid_url(self):
        """Test that an invalid URL returns an error."""
        result = scrape_text("not-a-valid-url")

        # Check that the scrape failed
        self.assertFalse(result["success"])

        # Check that an error message was returned
        self.assertIsNotNone(result["error"])

    def test_scrape_text_empty_url(self):
        """Test that an empty URL returns an error."""
        result = scrape_text("")

        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_scrape_text_returns_title(self):
        """Test that the page title is extracted."""
        result = scrape_text("https://example.com")

        if result["success"]:
            # example.com should have a title
            self.assertIsNotNone(result["title"])


class TestImageScraper(unittest.TestCase):
    """Tests for the image scraper module."""

    def test_scrape_images_valid_url(self):
        """Test that scraping images from a valid URL works."""
        result = scrape_images("https://example.com")

        # Check that the scrape succeeded
        self.assertTrue(result["success"])

        # Result should have an 'images' list (may be empty)
        self.assertIsInstance(result["images"], list)

        # Count should match the list length
        self.assertEqual(result["count"], len(result["images"]))

    def test_scrape_images_invalid_url(self):
        """Test that an invalid URL returns an error."""
        result = scrape_images("not-a-url")

        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_scrape_images_with_format_filter(self):
        """Test that format filtering works."""
        result = scrape_images("https://example.com", formats=[".jpg"])

        self.assertTrue(result["success"])
        # All images should be JPGs
        for image in result["images"]:
            self.assertTrue(
                image["src"].lower().endswith(".jpg") or
                image["src"].lower().endswith(".jpeg")
            )


class TestAudioScraper(unittest.TestCase):
    """Tests for the audio scraper module."""

    def test_scrape_audio_valid_url(self):
        """Test that scraping audio from a valid URL works."""
        result = scrape_audio("https://example.com")

        # Check structure (example.com has no audio, but should not error)
        self.assertTrue(result["success"])
        self.assertIsInstance(result["audio_files"], list)

    def test_scrape_audio_invalid_url(self):
        """Test that an invalid URL returns an error."""
        result = scrape_audio("bad-url")

        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])


class TestVideoScraper(unittest.TestCase):
    """Tests for the video scraper module."""

    def test_scrape_video_valid_url(self):
        """Test that scraping video from a valid URL works."""
        result = scrape_video("https://example.com")

        # Check structure (example.com has no video, but should not error)
        self.assertTrue(result["success"])
        self.assertIsInstance(result["video_files"], list)

    def test_scrape_video_invalid_url(self):
        """Test that an invalid URL returns an error."""
        result = scrape_video("invalid")

        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])


# This allows running the tests directly: python tests/test_scrapers.py
if __name__ == "__main__":
    unittest.main()
