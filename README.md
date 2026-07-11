# 🔮 morph

**A multi-modal web scraping package for Python.**

Extract text, images, audio, and video from any website. Convert media with OCR, speech recognition, and video processing.

---

## ✨ Features

- **📄 Text Scraping** — Extract all visible text from any webpage
- **🖼️ Image Scraping** — Find and download all images (JPG, PNG, etc.)
- **🎵 Audio Scraping** — Detect and download audio files (MP3, WAV)
- **🎬 Video Scraping** — Find and download video files (MP4, WEBM, MOV)
- **🔤 Image → Text** — OCR using Tesseract to read text from images
- **🎤 Audio → Text** — Speech recognition to transcribe audio
- **🎞️ Video Processing** — Extract audio, text, or frames from videos
- **📦 Export** — Save results as TXT, CSV, JSON, or ZIP
- **💻 CLI** — Full command-line interface
- **🌐 Web Interface** — Beautiful dark-themed browser UI

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/chiragferwani/morph.git
cd morph

# Install the package
pip install .

# Or install with all optional features
pip install ".[all]"
```

### Python API

```python
from morph import scrape_text, scrape_images

# Scrape text from a website
result = scrape_text("https://example.com")
print(result["text"])

# Scrape images
result = scrape_images("https://example.com")
for image in result["images"]:
    print(image["src"])
```

### CLI

```bash
# Scrape text
morph scrape text https://example.com --output json

# Scrape and download images
morph scrape images https://example.com --download

# Convert image to text (OCR)
morph convert image-to-text screenshot.png

# Start the web interface
morph web
```

### Web Interface

```bash
morph web --port 5000
```

Then open `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```
morph-nlp1/
├── morph/                    # Main package
│   ├── __init__.py           # Package init, exports all public functions
│   ├── cli/                  # Command-line interface
│   │   └── main.py           # CLI entry point (argparse)
│   ├── core/                 # Shared configuration
│   │   └── config.py         # Constants (timeouts, headers, formats)
│   ├── scrapers/             # Web scraping modules
│   │   ├── text_scraper.py   # scrape_text()
│   │   ├── image_scraper.py  # scrape_images()
│   │   ├── audio_scraper.py  # scrape_audio()
│   │   └── video_scraper.py  # scrape_video()
│   ├── converters/           # Media conversion modules
│   │   ├── image_converter.py # image_to_text() — OCR
│   │   ├── audio_converter.py # audio_to_text() — Speech Recognition
│   │   └── video_converter.py # video_to_audio/text/images()
│   ├── utils/                # Utility functions
│   │   ├── downloader.py     # download_file()
│   │   ├── exporter.py       # export_to_txt/csv/json/zip()
│   │   └── validator.py      # validate_url(), check_connection()
│   └── web/                  # Web interface
│       ├── app.py            # Flask backend
│       ├── templates/        # HTML templates
│       └── static/           # CSS and JavaScript
├── examples/                 # Usage examples
├── tests/                    # Unit tests
├── docs/                     # Documentation
├── setup.py                  # Installation script
├── pyproject.toml            # Modern packaging config
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

---

## 📋 Requirements

### Core (Required)
- Python 3.8+
- `requests` — HTTP library
- `beautifulsoup4` — HTML parser
- `flask` — Web framework

### Optional
- `pytesseract` + `Pillow` — For OCR (image to text)
- `SpeechRecognition` + `pydub` — For audio to text
- `moviepy` — For video processing

### System Dependencies
- **Tesseract OCR** — `sudo apt install tesseract-ocr`
- **FFmpeg** — `sudo apt install ffmpeg`

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request
