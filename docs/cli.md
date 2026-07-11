# CLI Documentation

## Overview

The `morph` command-line tool has three main commands:

| Command | Description |
|---------|-------------|
| `morph scrape` | Scrape content from a website |
| `morph convert` | Convert media files |
| `morph web` | Start the web interface |

## Scraping

### Scrape Text
```bash
morph scrape text https://example.com
morph scrape text https://example.com --output json
morph scrape text https://example.com --output csv
```

### Scrape Images
```bash
morph scrape images https://example.com
morph scrape images https://example.com --download
morph scrape images https://example.com --download --save-dir ./my_images
```

### Scrape Audio
```bash
morph scrape audio https://example.com
morph scrape audio https://example.com --download
```

### Scrape Video
```bash
morph scrape video https://example.com
morph scrape video https://example.com --download
```

## Converting

### Image to Text (OCR)
```bash
morph convert image-to-text photo.png
morph convert image-to-text photo.png --output json
```

### Audio to Text
```bash
morph convert audio-to-text recording.wav
morph convert audio-to-text recording.wav --output csv
```

### Video to Audio
```bash
morph convert video-to-audio video.mp4
morph convert video-to-audio video.mp4 --save-as audio.wav
```

### Video to Text
```bash
morph convert video-to-text video.mp4
```

### Video to Images (Frames)
```bash
morph convert video-to-images video.mp4
morph convert video-to-images video.mp4 --save-as ./frames/
```

## Web Interface

```bash
morph web                    # Start on default port 5000
morph web --port 8080        # Start on port 8080
morph web --debug            # Start with debug mode
```

## Global Options

```bash
morph --version              # Show version
morph --help                 # Show help
morph scrape --help          # Show scrape help
morph convert --help         # Show convert help
```
