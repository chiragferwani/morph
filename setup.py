"""
setup.py - Installation script for the morph package.

This file tells pip how to install the morph package,
what dependencies it needs, and how to register the CLI command.
"""

from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

# Read requirements from the requirements.txt file
with open("requirements.txt", "r", encoding="utf-8") as req_file:
    requirements = []
    for line in req_file:
        line = line.strip()
        # Skip empty lines and comments
        if line and not line.startswith("#"):
            requirements.append(line)

setup(
    # ---- Basic package information ----
    name="morphscrapper",
    version="0.1.3",
    author="Chirag",
    description="A multi-modal web scraping package for extracting text, images, audio, and video.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # ---- Find all sub-packages automatically ----
    packages=find_packages(),

    # ---- Dependencies ----
    install_requires=requirements,

    # ---- Include non-Python files (HTML, CSS, JS) ----
    include_package_data=True,
    package_data={
        "morph": [
            "web/templates/*.html",
            "web/static/*.css",
            "web/static/*.js",
            "web/static/*.png",
        ],
    },

    # ---- CLI entry point ----
    # This creates the 'morph' command when the package is installed
    entry_points={
        "console_scripts": [
            "morph=morph.cli.main:main",
        ],
    },

    # ---- PyPI classifiers ----
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    # ---- Minimum Python version ----
    python_requires=">=3.8",
)
