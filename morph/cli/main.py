"""
morph.cli.main - Command Line Interface for the morph web scraping package.

This module provides a user-friendly command-line tool for:
    - Scraping text, images, audio, and video from websites
    - Converting media files (OCR, speech-to-text, video processing)
    - Starting the web interface

Usage:
    morph scrape text https://example.com --output txt
    morph scrape images https://example.com --download
    morph convert image-to-text photo.jpg
    morph web --port 5000
"""

# 'argparse' is Python's built-in library for creating CLI tools
import argparse

# 'sys' is used to exit the program with status codes
import sys

# Import all our scraper functions
from morph.scrapers.text_scraper import scrape_text
from morph.scrapers.image_scraper import scrape_images
from morph.scrapers.audio_scraper import scrape_audio
from morph.scrapers.video_scraper import scrape_video

# Import all our converter functions
from morph.converters.image_converter import image_to_text
from morph.converters.audio_converter import audio_to_text
from morph.converters.video_converter import video_to_audio, video_to_text, video_to_images

# Import utility functions
from morph.utils.downloader import download_file
from morph.utils.exporter import export_to_txt, export_to_csv, export_to_json


def main():
    """
    Main entry point for the morph CLI.

    This function sets up the argument parser with all subcommands
    and dispatches to the appropriate handler function.
    """

    # ---- Create the top-level parser ----
    parser = argparse.ArgumentParser(
        prog="morph",
        description="morph - A multi-modal web scraping tool. "
                    "Scrape text, images, audio, and video from any website.",
    )

    # Add a version flag
    parser.add_argument(
        "--version",
        action="version",
        version="morph 0.1.0",
    )

    # ---- Create subcommands ----
    # This allows us to have "morph scrape", "morph convert", "morph web"
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
    )

    # ---- Set up the "scrape" command ----
    _setup_scrape_command(subparsers)

    # ---- Set up the "convert" command ----
    _setup_convert_command(subparsers)

    # ---- Set up the "web" command ----
    _setup_web_command(subparsers)

    # ---- Parse the arguments ----
    args = parser.parse_args()

    # If no command was given, show help
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # ---- Dispatch to the right handler ----
    if args.command == "scrape":
        _handle_scrape(args)
    elif args.command == "convert":
        _handle_convert(args)
    elif args.command == "web":
        _handle_web(args)


# ============================================================
# Command Setup Functions
# ============================================================

def _setup_scrape_command(subparsers):
    """
    Set up the 'scrape' subcommand with its arguments.

    This creates the argument parser for commands like:
        morph scrape text https://example.com
        morph scrape images https://example.com --download
    """
    scrape_parser = subparsers.add_parser(
        "scrape",
        help="Scrape content from a website",
    )

    # The type of content to scrape
    scrape_parser.add_argument(
        "type",
        choices=["text", "images", "audio", "video"],
        help="Type of content to scrape (text, images, audio, or video)",
    )

    # The URL to scrape from
    scrape_parser.add_argument(
        "url",
        help="URL of the website to scrape",
    )

    # Output format for text scraping
    scrape_parser.add_argument(
        "--output", "-o",
        choices=["txt", "csv", "json"],
        default="txt",
        help="Output format for text (default: txt)",
    )

    # Flag to download found media files
    scrape_parser.add_argument(
        "--download", "-d",
        action="store_true",
        help="Download found media files",
    )

    # Directory to save downloads
    scrape_parser.add_argument(
        "--save-dir", "-s",
        default=None,
        help="Directory to save downloaded files (default: morph_downloads)",
    )


def _setup_convert_command(subparsers):
    """
    Set up the 'convert' subcommand with its arguments.

    This creates the argument parser for commands like:
        morph convert image-to-text photo.jpg
        morph convert audio-to-text recording.wav
    """
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert media files (OCR, speech-to-text, video processing)",
    )

    # The type of conversion to perform
    convert_parser.add_argument(
        "type",
        choices=[
            "image-to-text",
            "audio-to-text",
            "video-to-audio",
            "video-to-text",
            "video-to-images",
        ],
        help="Type of conversion to perform",
    )

    # The input file to convert
    convert_parser.add_argument(
        "file",
        help="Path to the input file",
    )

    # Output format for text conversions
    convert_parser.add_argument(
        "--output", "-o",
        choices=["txt", "csv", "json"],
        default="txt",
        help="Output format for text results (default: txt)",
    )

    # Output file path
    convert_parser.add_argument(
        "--save-as",
        default=None,
        help="Path to save the output file",
    )


def _setup_web_command(subparsers):
    """
    Set up the 'web' subcommand for launching the web interface.

    This creates the argument parser for:
        morph web
        morph web --port 8080
    """
    web_parser = subparsers.add_parser(
        "web",
        help="Start the web interface",
    )

    # Port number for the web server
    web_parser.add_argument(
        "--port", "-p",
        type=int,
        default=5000,
        help="Port to run the web server on (default: 5000)",
    )

    # Whether to enable debug mode
    web_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )


# ============================================================
# Command Handler Functions
# ============================================================

def _handle_scrape(args):
    """
    Handle the 'scrape' command by calling the appropriate scraper.

    Parameters:
        args: Parsed command-line arguments.
    """
    print(f"\n🔍 Scraping {args.type} from: {args.url}\n")

    # ---- Scrape Text ----
    if args.type == "text":
        result = scrape_text(args.url)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        # Display the results
        print(f"📄 Title: {result['title']}")
        print(f"📊 Words found: {result['word_count']}")
        print(f"\n--- Extracted Text ---\n")
        print(result["text"][:2000])  # Show first 2000 characters

        if len(result["text"]) > 2000:
            print(f"\n... (showing first 2000 of {len(result['text'])} characters)")

        # Export to the requested format
        _export_text_result(result["text"], args.output, args.url)

    # ---- Scrape Images ----
    elif args.type == "images":
        result = scrape_images(args.url)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        print(f"🖼️  Found {result['count']} images\n")

        # List all found images
        for i, image in enumerate(result["images"]):
            print(f"  {i + 1}. {image['filename']} - {image['src']}")

        # Download if requested
        if args.download:
            _download_media_files(result["images"], args.save_dir)

    # ---- Scrape Audio ----
    elif args.type == "audio":
        result = scrape_audio(args.url)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        print(f"🎵 Found {result['count']} audio files\n")

        for i, audio in enumerate(result["audio_files"]):
            print(f"  {i + 1}. {audio['filename']} - {audio['src']}")

        if args.download:
            _download_media_files(result["audio_files"], args.save_dir)

    # ---- Scrape Video ----
    elif args.type == "video":
        result = scrape_video(args.url)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        print(f"🎬 Found {result['count']} video files\n")

        for i, video in enumerate(result["video_files"]):
            print(f"  {i + 1}. {video['filename']} - {video['src']}")

        if args.download:
            _download_media_files(result["video_files"], args.save_dir)

    print("\n✅ Done!")


def _handle_convert(args):
    """
    Handle the 'convert' command by calling the appropriate converter.

    Parameters:
        args: Parsed command-line arguments.
    """
    print(f"\n🔄 Converting: {args.file}\n")

    # ---- Image to Text (OCR) ----
    if args.type == "image-to-text":
        result = image_to_text(args.file)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        print(f"📊 Words found: {result['word_count']}")
        print(f"\n--- Extracted Text ---\n")
        print(result["text"])

        # Export if save-as is specified or use default
        _export_text_result(result["text"], args.output, args.file)

    # ---- Audio to Text ----
    elif args.type == "audio-to-text":
        result = audio_to_text(args.file)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        print(f"📊 Words found: {result['word_count']}")
        print(f"\n--- Transcribed Text ---\n")
        print(result["text"])

        _export_text_result(result["text"], args.output, args.file)

    # ---- Video to Audio ----
    elif args.type == "video-to-audio":
        output_path = args.save_as
        result = video_to_audio(args.file, output_path)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        print(f"🎵 Audio saved to: {result['audio_path']}")

    # ---- Video to Text ----
    elif args.type == "video-to-text":
        result = video_to_text(args.file)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        print(f"📊 Words found: {result['word_count']}")
        print(f"\n--- Transcribed Text ---\n")
        print(result["text"])

        _export_text_result(result["text"], args.output, args.file)

    # ---- Video to Images ----
    elif args.type == "video-to-images":
        result = video_to_images(args.file, args.save_as)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            sys.exit(1)

        print(f"🖼️  Extracted {result['count']} frames")
        for frame_path in result["frames"][:10]:
            print(f"  - {frame_path}")

        if result["count"] > 10:
            print(f"  ... and {result['count'] - 10} more")

    print("\n✅ Done!")


def _handle_web(args):
    """
    Handle the 'web' command by starting the Flask web interface.

    Parameters:
        args: Parsed command-line arguments.
    """
    print(f"\n🌐 Starting morph web interface on port {args.port}...")
    print(f"   Open http://localhost:{args.port} in your browser\n")

    # Import and run the Flask app
    from morph.web.app import create_app

    app = create_app()
    app.run(host="0.0.0.0", port=args.port, debug=args.debug)


# ============================================================
# Helper Functions
# ============================================================

def _export_text_result(text, output_format, source_name):
    """
    Export text results to a file in the specified format.

    Parameters:
        text (str): The text to export.
        output_format (str): The format ('txt', 'csv', or 'json').
        source_name (str): Name of the source (URL or file) for the output filename.
    """
    # Create a safe filename from the source
    safe_name = source_name.replace("://", "_").replace("/", "_").replace(".", "_")

    # Limit filename length
    if len(safe_name) > 50:
        safe_name = safe_name[:50]

    if output_format == "txt":
        file_path = f"{safe_name}_output.txt"
        result = export_to_txt(text, file_path)
    elif output_format == "csv":
        file_path = f"{safe_name}_output.csv"
        # Split text into lines for CSV rows
        lines = text.split("\n")
        result = export_to_csv(lines, file_path, headers=["text"])
    elif output_format == "json":
        file_path = f"{safe_name}_output.json"
        data = {"source": source_name, "text": text}
        result = export_to_json(data, file_path)
    else:
        return

    if result["success"]:
        print(f"\n💾 Saved to: {result['file_path']}")
    else:
        print(f"\n⚠️  Could not save: {result['error']}")


def _download_media_files(media_list, save_dir):
    """
    Download a list of media files.

    Parameters:
        media_list (list): List of dicts with 'src' and 'filename' keys.
        save_dir (str or None): Directory to save files to.
    """
    print(f"\n📥 Downloading {len(media_list)} files...\n")

    success_count = 0
    fail_count = 0

    for i, media in enumerate(media_list):
        print(f"  [{i + 1}/{len(media_list)}] Downloading {media['filename']}...", end=" ")

        result = download_file(media["src"], save_dir=save_dir)

        if result["success"]:
            print(f"✅ ({result['file_size']} bytes)")
            success_count = success_count + 1
        else:
            print(f"❌ {result['error']}")
            fail_count = fail_count + 1

    print(f"\n📊 Downloaded: {success_count} successful, {fail_count} failed")


# ---- Entry point ----
# This allows running: python -m morph.cli.main
if __name__ == "__main__":
    main()
