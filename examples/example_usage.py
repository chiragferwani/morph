"""
example_usage.py - Demonstrates how to use the morph package.

This file shows simple examples for each feature of the morph package.
Run this file to see the package in action.

Usage:
    python examples/example_usage.py
"""

# ============================================================
# Example 1: Scrape text from a website
# ============================================================

print("=" * 60)
print("Example 1: Scraping text from example.com")
print("=" * 60)

# Import the scrape_text function
from morph import scrape_text

# Scrape text from example.com
result = scrape_text("https://example.com")

# Check if it worked
if result["success"]:
    print(f"✅ Title: {result['title']}")
    print(f"📊 Word count: {result['word_count']}")
    print(f"📄 First 200 characters:")
    print(result["text"][:200])
else:
    print(f"❌ Error: {result['error']}")

print()


# ============================================================
# Example 2: Scrape images from a website
# ============================================================

print("=" * 60)
print("Example 2: Scraping images from example.com")
print("=" * 60)

# Import the scrape_images function
from morph import scrape_images

# Scrape images
result = scrape_images("https://example.com")

if result["success"]:
    print(f"🖼️  Found {result['count']} images")
    for image in result["images"]:
        print(f"  - {image['filename']}: {image['src']}")
else:
    print(f"❌ Error: {result['error']}")

print()


# ============================================================
# Example 3: Validate a URL
# ============================================================

print("=" * 60)
print("Example 3: Validating URLs")
print("=" * 60)

# Import the validate_url function
from morph import validate_url

# Test some URLs
urls_to_test = [
    "https://example.com",
    "http://google.com",
    "not-a-url",
    "ftp://files.example.com",
    "",
]

for url in urls_to_test:
    is_valid = validate_url(url)
    status = "✅ Valid" if is_valid else "❌ Invalid"
    print(f"  {status}: {url if url else '(empty string)'}")

print()


# ============================================================
# Example 4: Export data to different formats
# ============================================================

print("=" * 60)
print("Example 4: Exporting data to files")
print("=" * 60)

# Import export functions
from morph import export_to_txt, export_to_json

# Export text to a file
text_result = export_to_txt("Hello from morph!", "example_output.txt")
if text_result["success"]:
    print(f"💾 Text saved to: {text_result['file_path']}")

# Export data to JSON
data = {
    "tool": "morph",
    "version": "0.1.0",
    "features": ["text", "images", "audio", "video"],
}
json_result = export_to_json(data, "example_output.json")
if json_result["success"]:
    print(f"💾 JSON saved to: {json_result['file_path']}")

print()


# ============================================================
# Example 5: Check website connection
# ============================================================

print("=" * 60)
print("Example 5: Checking website connections")
print("=" * 60)

# Import the check_connection function
from morph import check_connection

# Check if some websites are reachable
sites = ["https://example.com", "https://httpstat.us/404"]

for site in sites:
    result = check_connection(site)
    if result["reachable"]:
        print(f"  ✅ {site} - Status: {result['status_code']}")
    else:
        print(f"  ❌ {site} - {result['error']}")

print()
print("=" * 60)
print("All examples completed!")
print("=" * 60)
