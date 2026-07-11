"""
test_utils.py - Unit tests for the morph utility modules.

These tests check the validator, downloader, and exporter functions.

Run with: python -m pytest tests/test_utils.py -v
"""

import unittest
import os
import json
import tempfile
import shutil

# Import the utility functions
from morph.utils.validator import validate_url, check_connection
from morph.utils.exporter import export_to_txt, export_to_csv, export_to_json, export_to_zip


class TestValidator(unittest.TestCase):
    """Tests for the URL validator."""

    def test_valid_http_url(self):
        """Test that a valid HTTP URL is accepted."""
        self.assertTrue(validate_url("http://example.com"))

    def test_valid_https_url(self):
        """Test that a valid HTTPS URL is accepted."""
        self.assertTrue(validate_url("https://example.com"))

    def test_url_with_path(self):
        """Test that a URL with a path is accepted."""
        self.assertTrue(validate_url("https://example.com/page/about"))

    def test_invalid_url_no_scheme(self):
        """Test that a URL without http/https is rejected."""
        self.assertFalse(validate_url("example.com"))

    def test_invalid_url_ftp(self):
        """Test that FTP URLs are rejected (we only support HTTP/HTTPS)."""
        self.assertFalse(validate_url("ftp://example.com"))

    def test_empty_url(self):
        """Test that an empty string is rejected."""
        self.assertFalse(validate_url(""))

    def test_random_text(self):
        """Test that random text is rejected."""
        self.assertFalse(validate_url("not a url at all"))

    def test_check_connection_valid(self):
        """Test checking connection to a real website."""
        result = check_connection("https://example.com")

        self.assertTrue(result["reachable"])
        self.assertEqual(result["status_code"], 200)

    def test_check_connection_invalid_url(self):
        """Test that invalid URLs return an appropriate error."""
        result = check_connection("not-a-url")

        self.assertFalse(result["reachable"])
        self.assertIsNotNone(result["error"])


class TestExporter(unittest.TestCase):
    """Tests for the data exporter functions."""

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Remove the temporary directory after tests."""
        shutil.rmtree(self.test_dir)

    def test_export_to_txt_string(self):
        """Test exporting a string to a TXT file."""
        file_path = os.path.join(self.test_dir, "test.txt")
        result = export_to_txt("Hello, World!", file_path)

        # Check that export succeeded
        self.assertTrue(result["success"])

        # Check that the file was created
        self.assertTrue(os.path.exists(file_path))

        # Check the file content
        with open(file_path, "r") as f:
            content = f.read()
        self.assertEqual(content, "Hello, World!")

    def test_export_to_txt_list(self):
        """Test exporting a list of strings to a TXT file."""
        file_path = os.path.join(self.test_dir, "test_list.txt")
        result = export_to_txt(["line 1", "line 2", "line 3"], file_path)

        self.assertTrue(result["success"])

        with open(file_path, "r") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 3)

    def test_export_to_csv(self):
        """Test exporting data to a CSV file."""
        file_path = os.path.join(self.test_dir, "test.csv")
        data = [["name", "age"], ["Alice", "30"], ["Bob", "25"]]
        result = export_to_csv(data, file_path)

        self.assertTrue(result["success"])
        self.assertTrue(os.path.exists(file_path))

    def test_export_to_json(self):
        """Test exporting data to a JSON file."""
        file_path = os.path.join(self.test_dir, "test.json")
        data = {"name": "morph", "version": "0.1.0"}
        result = export_to_json(data, file_path)

        self.assertTrue(result["success"])

        # Verify the JSON content
        with open(file_path, "r") as f:
            loaded = json.load(f)
        self.assertEqual(loaded["name"], "morph")

    def test_export_to_zip(self):
        """Test creating a ZIP archive."""
        # First create some files to zip
        file1 = os.path.join(self.test_dir, "file1.txt")
        file2 = os.path.join(self.test_dir, "file2.txt")

        with open(file1, "w") as f:
            f.write("File 1 content")
        with open(file2, "w") as f:
            f.write("File 2 content")

        # Create the zip
        zip_path = os.path.join(self.test_dir, "test.zip")
        result = export_to_zip([file1, file2], zip_path)

        self.assertTrue(result["success"])
        self.assertTrue(os.path.exists(zip_path))


# This allows running the tests directly: python tests/test_utils.py
if __name__ == "__main__":
    unittest.main()
