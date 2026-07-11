# API Reference

## Scrapers

### `scrape_text(url)`
Extract all visible text from a webpage.

**Parameters:**
- `url` (str): The URL to scrape.

**Returns:** dict with keys: `success`, `url`, `title`, `text`, `word_count`, `error`

---

### `scrape_images(url, formats=None)`
Extract all image URLs from a webpage.

**Parameters:**
- `url` (str): The URL to scrape.
- `formats` (list, optional): Filter by extensions, e.g. `['.jpg', '.png']`

**Returns:** dict with keys: `success`, `url`, `images` (list of dicts), `count`, `error`

Each image dict has: `src`, `alt`, `filename`

---

### `scrape_audio(url, formats=None)`
Extract all audio file URLs from a webpage.

**Parameters:**
- `url` (str): The URL to scrape.
- `formats` (list, optional): Filter by extensions, e.g. `['.mp3']`

**Returns:** dict with keys: `success`, `url`, `audio_files`, `count`, `error`

---

### `scrape_video(url, formats=None)`
Extract all video file URLs from a webpage.

**Parameters:**
- `url` (str): The URL to scrape.
- `formats` (list, optional): Filter by extensions, e.g. `['.mp4']`

**Returns:** dict with keys: `success`, `url`, `video_files`, `count`, `error`

---

## Converters

### `image_to_text(image_path)`
Extract text from an image using OCR.

**Parameters:**
- `image_path` (str): Path to the image file.

**Returns:** dict with keys: `success`, `image_path`, `text`, `word_count`, `error`

**Requires:** pytesseract, Pillow, Tesseract OCR

---

### `audio_to_text(audio_path)`
Transcribe an audio file to text using speech recognition.

**Parameters:**
- `audio_path` (str): Path to the audio file (WAV or MP3).

**Returns:** dict with keys: `success`, `audio_path`, `text`, `word_count`, `error`

**Requires:** SpeechRecognition, pydub (for MP3)

---

### `video_to_audio(video_path, output_path=None)`
Extract the audio track from a video file.

**Parameters:**
- `video_path` (str): Path to the video file.
- `output_path` (str, optional): Where to save the audio (default: same name with .wav).

**Returns:** dict with keys: `success`, `video_path`, `audio_path`, `error`

**Requires:** moviepy

---

### `video_to_text(video_path)`
Transcribe a video's audio to text.

**Parameters:**
- `video_path` (str): Path to the video file.

**Returns:** dict with keys: `success`, `video_path`, `text`, `word_count`, `error`

---

### `video_to_images(video_path, output_dir=None, interval=None)`
Extract frames from a video at regular intervals.

**Parameters:**
- `video_path` (str): Path to the video file.
- `output_dir` (str, optional): Where to save frames.
- `interval` (float, optional): Seconds between frames (default: 1.0).

**Returns:** dict with keys: `success`, `video_path`, `frames`, `count`, `error`

---

## Utilities

### `validate_url(url)` → bool
Check if a URL is valid (has http/https scheme and network location).

### `check_connection(url)` → dict
Check if a website is reachable. Returns `reachable`, `status_code`, `error`.

### `download_file(url, save_path=None, save_dir=None)` → dict
Download a file from a URL. Returns `success`, `file_path`, `file_size`, `error`.

### `export_to_txt(data, file_path)` → dict
Export text data to a .txt file.

### `export_to_csv(data, file_path, headers=None)` → dict
Export data to a .csv file.

### `export_to_json(data, file_path)` → dict
Export data to a .json file.

### `export_to_zip(file_paths, zip_path)` → dict
Create a ZIP archive from a list of files.
