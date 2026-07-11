"""
test_converters.py - Unit tests for the morph converter modules.

These tests check that the converter functions handle edge cases properly.
Note: Full conversion tests require external tools (Tesseract, FFmpeg).

Run with: python -m pytest tests/test_converters.py -v
"""

import unittest
import os

# Import the converter functions
from morph.converters.image_converter import image_to_text
from morph.converters.audio_converter import audio_to_text
from morph.converters.video_converter import video_to_audio, video_to_text, video_to_images


class TestImageConverter(unittest.TestCase):
    """Tests for the image-to-text converter."""

    def test_image_to_text_missing_file(self):
        """Test that a missing image file returns a clear error."""
        result = image_to_text("nonexistent_image.jpg")

        # Should fail because either the file doesn't exist
        # or the OCR library isn't installed — both are valid failures
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_image_to_text_returns_dict(self):
        """Test that the function returns a properly structured dictionary."""
        result = image_to_text("fake.jpg")

        # Check that all expected keys are present
        self.assertIn("success", result)
        self.assertIn("image_path", result)
        self.assertIn("text", result)
        self.assertIn("word_count", result)
        self.assertIn("error", result)


class TestAudioConverter(unittest.TestCase):
    """Tests for the audio-to-text converter."""

    def test_audio_to_text_missing_file(self):
        """Test that a missing audio file returns a clear error."""
        result = audio_to_text("nonexistent_audio.wav")

        # Should fail — either file not found or library not installed
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_audio_to_text_returns_dict(self):
        """Test that the function returns a properly structured dictionary."""
        result = audio_to_text("fake.wav")

        # Check that all expected keys are present
        self.assertIn("success", result)
        self.assertIn("audio_path", result)
        self.assertIn("text", result)
        self.assertIn("word_count", result)
        self.assertIn("error", result)


class TestVideoConverter(unittest.TestCase):
    """Tests for the video converter functions."""

    def test_video_to_audio_missing_file(self):
        """Test that a missing video file returns a clear error."""
        result = video_to_audio("nonexistent_video.mp4")

        # Should fail — either file not found or library not installed
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_video_to_text_missing_file(self):
        """Test that a missing video file returns a clear error."""
        result = video_to_text("nonexistent_video.mp4")

        self.assertFalse(result["success"])

    def test_video_to_images_missing_file(self):
        """Test that a missing video file returns a clear error."""
        result = video_to_images("nonexistent_video.mp4")

        # Should fail — either file not found or library not installed
        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])

    def test_video_to_audio_returns_dict(self):
        """Test that video_to_audio returns a properly structured dict."""
        result = video_to_audio("fake.mp4")

        self.assertIn("success", result)
        self.assertIn("video_path", result)
        self.assertIn("audio_path", result)
        self.assertIn("error", result)

    def test_video_to_images_returns_dict(self):
        """Test that video_to_images returns a properly structured dict."""
        result = video_to_images("fake.mp4")

        self.assertIn("success", result)
        self.assertIn("video_path", result)
        self.assertIn("frames", result)
        self.assertIn("count", result)
        self.assertIn("error", result)


# This allows running the tests directly: python tests/test_converters.py
if __name__ == "__main__":
    unittest.main()
