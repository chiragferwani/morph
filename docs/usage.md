# Usage Guide

## Python API

### Scraping Text

```python
from morph import scrape_text

result = scrape_text("https://example.com")

if result["success"]:
    print(result["title"])       # Page title
    print(result["text"])        # Extracted text
    print(result["word_count"])  # Number of words
else:
    print(result["error"])       # Error message
```

### Scraping Images

```python
from morph import scrape_images

result = scrape_images("https://example.com")

for image in result["images"]:
    print(image["src"])       # Image URL
    print(image["filename"])  # Filename
    print(image["alt"])       # Alt text
```

### Scraping Audio

```python
from morph import scrape_audio

result = scrape_audio("https://example.com")

for audio in result["audio_files"]:
    print(audio["src"])       # Audio file URL
    print(audio["filename"])  # Filename
```

### Scraping Video

```python
from morph import scrape_video

result = scrape_video("https://example.com")

for video in result["video_files"]:
    print(video["src"])       # Video file URL
    print(video["filename"])  # Filename
```

### Image to Text (OCR)

```python
from morph import image_to_text

result = image_to_text("screenshot.png")

if result["success"]:
    print(result["text"])        # Extracted text
    print(result["word_count"])  # Word count
```

### Audio to Text

```python
from morph import audio_to_text

result = audio_to_text("recording.wav")

if result["success"]:
    print(result["text"])  # Transcribed text
```

### Video Processing

```python
from morph import video_to_audio, video_to_text, video_to_images

# Extract audio from video
result = video_to_audio("video.mp4")
print(result["audio_path"])  # Path to extracted audio

# Transcribe video speech
result = video_to_text("video.mp4")
print(result["text"])

# Extract frames
result = video_to_images("video.mp4", interval=2.0)
print(result["frames"])  # List of frame paths
```

### Exporting Data

```python
from morph import export_to_txt, export_to_csv, export_to_json, export_to_zip

# Export to TXT
export_to_txt("Hello, world!", "output.txt")

# Export to CSV
export_to_csv([["Name", "Age"], ["Alice", "30"]], "output.csv")

# Export to JSON
export_to_json({"key": "value"}, "output.json")

# Export to ZIP
export_to_zip(["file1.txt", "file2.txt"], "archive.zip")
```

### Downloading Files

```python
from morph import download_file

result = download_file("https://example.com/image.jpg")

if result["success"]:
    print(f"Saved to: {result['file_path']}")
    print(f"Size: {result['file_size']} bytes")
```
