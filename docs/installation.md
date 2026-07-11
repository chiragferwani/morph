# Installation Guide

## Prerequisites

- **Python 3.8 or higher** — Check with `python --version`
- **pip** — Python package manager (comes with Python)

## Install from Source

```bash
# 1. Clone the repository
git clone https://github.com/chiragferwani/morph.git
cd morph

# 2. Install the package
pip install .
```

## Install with Optional Features

```bash
# Install with OCR support (image to text)
pip install ".[ocr]"

# Install with audio processing
pip install ".[audio]"

# Install with video processing
pip install ".[video]"

# Install everything
pip install ".[all]"
```

## System Dependencies

### Tesseract OCR (for image-to-text)

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

# macOS
brew install tesseract
```

### FFmpeg (for audio/video processing)

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

## Verify Installation

```bash
# Check that the CLI works
morph --version

# Should output: morph 0.1.0
```

```python
# Check that the Python package works
import morph
print(morph.__version__)
```
