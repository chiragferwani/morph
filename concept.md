# Prompt: Build a Python Multi-Modal Web Scraping Package

You are an expert Python software engineer, package maintainer, and web scraping developer.

Your task is to build a complete production-ready Python project from scratch.

## Project Goal

Develop a Python package that can scrape and extract multiple types of web content from a given website URL.

The package should focus on simplicity, readability, and educational code.

Every line of code should be easy to understand.

Avoid unnecessarily complex programming techniques.

Avoid writing long one-line expressions.

Write beginner-friendly Python.

Every function should perform only one task.

Use meaningful variable names.

Add comments explaining every important step.

---

# Project Name

**morph**

---

# Main Features

The user enters

* Website URL
* Content Type
* Output Format

The package then extracts and converts the requested information.

---

# Main Menu

The project must support four primary scraping modes.

## 1. Text

Extract all visible text from the webpage.

Store the text in raw form.

Allow exporting into

* TXT
* JSON
* CSV

---

## 2. Images

Extract every image available on the webpage.

Support

* JPG
* PNG

Allow downloading all images.

Maintain original filenames whenever possible.

---

## 3. Audio

Extract every audio resource from the webpage.

Support

* MP3
* WAV

Allow downloading all detected audio files.

---

## 4. Video

Extract every video resource.

Support

* MP4
* MOV
* WEBM

Allow downloading all videos.

---

# Advanced Conversion Menu

The package must also include conversion utilities.

## Image

Convert image into

* Text (OCR)

Export OCR text as

* TXT
* CSV
* JSON

---

## Audio

Convert audio into

* Text

Export as

* TXT
* CSV
* JSON

---

## Video

Allow extracting

* Frames (Images)
* Audio
* Text (using speech recognition)

Export each result independently.

---

# Folder Structure

Create a clean professional project structure.

Include

package/

cli/

core/

scrapers/

converters/

utils/

examples/

tests/

docs/

web/

README.md

LICENSE

CHANGELOG.md

setup.py

pyproject.toml

requirements.txt

---

# Python Package

The project must be installable using

pip install .

The package should expose simple functions like

scrape_text()

scrape_images()

scrape_audio()

scrape_video()

image_to_text()

audio_to_text()

video_to_audio()

video_to_text()

video_to_images()

---

# Command Line Interface

Create a CLI.

Example

project scrape

project convert

project download

project export

Provide help menus.

---

# HTML Web Interface

Create a simple responsive HTML interface.

No React.

No Angular.

No Vue.

Use only

HTML

CSS

Vanilla JavaScript

Python backend

The webpage should contain

Website URL input

Dropdown for content type

Dropdown for output format

Start Scraping button

Progress indicator

Download button

Result preview

Image gallery

Scrollable text viewer

Audio player

Video player

Status messages

---

# Backend

Use Python backend.

Keep routing simple.

Organize code cleanly.

Separate frontend and backend.

Return JSON responses.

---

# Code Style

**The code must be simple and easily understandable.**

**For every function or block of code, add clear comments explaining what it does and why.**

Every function should be small.

Every function should have a docstring.

Add inline comments for every important step.

Avoid unnecessary object-oriented programming.

Use simple loops.

Keep logic readable.

Prioritize clarity over cleverness.

Write code that a beginner can read and understand without external help.

---

# Error Handling

Handle

Invalid URL

Network failure

Unsupported website

Missing media

Timeout

Permission errors

File write errors

Gracefully display user-friendly messages.

---

# Export Features

Allow exporting into

TXT

CSV

JSON

Images

Audio

Video

ZIP archive

---

# Documentation

Generate

README.md

Installation guide

Usage examples

CLI documentation

API documentation

Developer guide

Package publishing guide

---

# Testing

Create unit tests.

Provide sample URLs.

Include expected outputs.

---

# Packaging

Generate everything required for publishing on PyPI.

Include

setup.py

pyproject.toml

MANIFEST.in

requirements.txt

License

Versioning

Proper package metadata

Example

pip install project-name

---

# Final Deliverables

Produce a complete project with

Clean architecture

Well-organized folders

Fully commented code

Professional documentation

Working HTML interface

CLI

Python package

Ready for GitHub

Ready for PyPI publication

Every generated file should be complete and directly runnable without placeholders or TODOs.
