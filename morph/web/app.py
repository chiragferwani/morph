"""
morph.web.app - Flask web backend for the morph scraping interface.

This module creates a simple Flask web server that:
    - Serves the HTML interface at the root URL (/)
    - Provides a JSON API for scraping at /api/scrape
    - Provides a JSON API for converting at /api/convert
    - Allows downloading scraped files at /api/download/<filename>

The web interface lets users enter a URL, select content type,
and scrape content through a neo-brutalism themed UI.
"""

import os
import json
import tempfile

# 'Flask' is a lightweight web framework for Python
from flask import Flask, render_template, request, jsonify, send_file

# Import our scraper functions
from morph.scrapers.text_scraper import scrape_text
from morph.scrapers.image_scraper import scrape_images
from morph.scrapers.audio_scraper import scrape_audio
from morph.scrapers.video_scraper import scrape_video

# Import our converter functions
from morph.converters.image_converter import image_to_text
from morph.converters.audio_converter import audio_to_text
from morph.converters.video_converter import video_to_audio, video_to_text, video_to_images

# Import our exporter functions
from morph.utils.exporter import export_to_txt, export_to_csv, export_to_json


def create_app():
    """
    Create and configure the Flask web application.

    This function:
        1. Creates a new Flask app
        2. Sets up the template and static file directories
        3. Registers all the URL routes (scraping + converting)
        4. Returns the configured app

    Returns:
        Flask: A configured Flask application ready to run.
    """

    # ---- Step 1: Figure out paths for templates and static files ----
    # Get the directory where this file (app.py) is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Templates are in the 'templates' subfolder
    template_dir = os.path.join(current_dir, "templates")

    # Static files (CSS, JS, images) are in the 'static' subfolder
    static_dir = os.path.join(current_dir, "static")

    # ---- Step 2: Create the Flask app ----
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
    )

    # Create a temporary directory for storing scraped results
    app.config["RESULTS_DIR"] = tempfile.mkdtemp(prefix="morph_results_")

    # Create an uploads directory for converter input files
    app.config["UPLOADS_DIR"] = tempfile.mkdtemp(prefix="morph_uploads_")

    # ---- Step 3: Register routes ----

    @app.route("/")
    def index():
        """
        Serve the main HTML interface.

        This is what the user sees when they visit http://localhost:5000/
        """
        return render_template("index.html")

    @app.route("/api/scrape", methods=["POST"])
    def api_scrape():
        """
        API endpoint for scraping content from a URL.

        Expects a JSON body with:
            - 'url' (str): The URL to scrape
            - 'content_type' (str): One of 'text', 'images', 'audio', 'video'
            - 'output_format' (str, optional): 'txt', 'csv', or 'json'

        Returns:
            JSON response with the scraping results.
        """
        # ---- Parse the request data ----
        data = request.get_json()

        # Check that required fields are present
        if not data:
            return jsonify({"success": False, "error": "No data provided."}), 400

        url = data.get("url", "")
        content_type = data.get("content_type", "")
        output_format = data.get("output_format", "json")

        # Validate that URL and content_type were provided
        if not url:
            return jsonify({"success": False, "error": "URL is required."}), 400

        if not content_type:
            return jsonify({"success": False, "error": "Content type is required."}), 400

        # ---- Call the appropriate scraper ----
        if content_type == "text":
            result = scrape_text(url)

            # If successful, save to file (including JSON output format)
            if result["success"]:
                file_path = _save_text_result(
                    result["text"], output_format, app.config["RESULTS_DIR"]
                )
                result["download_file"] = os.path.basename(file_path) if file_path else None

        elif content_type == "images":
            result = scrape_images(url)

        elif content_type == "audio":
            result = scrape_audio(url)

        elif content_type == "video":
            result = scrape_video(url)

        else:
            return jsonify({
                "success": False,
                "error": f"Unknown content type: '{content_type}'. "
                         f"Use: text, images, audio, or video.",
            }), 400

        # Return the result as JSON
        return jsonify(result)

    @app.route("/api/zip_media", methods=["POST"])
    def api_zip_media():
        """
        API endpoint to download and zip scraped media resources on demand.

        Expects a JSON body with:
            - 'content_type': 'images', 'audio', or 'video'
            - 'media': list of dictionaries containing 'src' and 'filename'
            - 'output_format': the selected output format filter
        """
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided."}), 400

        content_type = data.get("content_type", "")
        media_list = data.get("media", [])
        output_format = data.get("output_format", "zip")

        if not media_list:
            return jsonify({"success": False, "error": "No media items to download."}), 400

        # ---- Filter media files by extension if needed ----
        filtered_list = []
        for item in media_list:
            src = item.get("src", "")
            filename = item.get("filename", "")
            if not src:
                continue

            ext = src.lower().split("?")[0].split(".")[-1]
            
            if content_type == "images" and output_format in ["jpg", "png"]:
                if output_format == "jpg" and ext in ["jpg", "jpeg"]:
                    filtered_list.append(item)
                elif output_format == "png" and ext == "png":
                    filtered_list.append(item)
            elif content_type == "audio" and output_format in ["mp3", "wav"]:
                if output_format == "mp3" and ext == "mp3":
                    filtered_list.append(item)
                elif output_format == "wav" and ext == "wav":
                    filtered_list.append(item)
            elif content_type == "video" and output_format in ["mp4", "webm"]:
                if output_format == "mp4" and ext == "mp4":
                    filtered_list.append(item)
                elif output_format == "webm" and ext == "webm":
                    filtered_list.append(item)
            else:
                # 'zip' or all other cases get included
                filtered_list.append(item)

        if not filtered_list:
            return jsonify({"success": False, "error": f"No items matched the format '{output_format}'."}), 400

        # ---- Download and ZIP ----
        from morph.utils.downloader import download_file
        from morph.utils.exporter import export_to_zip

        zip_filename = f"scraped_{content_type}.zip"
        zip_path = os.path.join(app.config["RESULTS_DIR"], zip_filename)
        temp_subfolder = tempfile.mkdtemp(dir=app.config["RESULTS_DIR"])
        downloaded_paths = []

        for item in filtered_list:
            dl_res = download_file(item["src"], save_dir=temp_subfolder)
            if dl_res["success"]:
                downloaded_paths.append(dl_res["file_path"])

        if not downloaded_paths:
            return jsonify({"success": False, "error": "Failed to download any media files."}), 500

        zip_res = export_to_zip(downloaded_paths, zip_path)
        if not zip_res["success"]:
            return jsonify({"success": False, "error": f"Failed to create ZIP: {zip_res['error']}"}), 500

        return jsonify({
            "success": True,
            "download_file": zip_filename
        })

    @app.route("/api/convert", methods=["POST"])
    def api_convert():
        """
        API endpoint for converting uploaded files.

        Expects a multipart form with:
            - 'file': The uploaded file
            - 'conversion_type': One of 'image-to-text', 'audio-to-text',
              'video-to-audio', 'video-to-text', 'video-to-images'
            - 'output_format' (optional): 'txt', 'csv', or 'json'

        Returns:
            JSON response with the conversion results.
        """
        # ---- Check that a file was uploaded ----
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No file uploaded."}), 400

        uploaded_file = request.files["file"]
        conversion_type = request.form.get("conversion_type", "")
        output_format = request.form.get("output_format", "txt")

        # Check that a file was actually selected
        if uploaded_file.filename == "":
            return jsonify({"success": False, "error": "No file selected."}), 400

        if not conversion_type:
            return jsonify({"success": False, "error": "Conversion type is required."}), 400

        # ---- Save the uploaded file temporarily ----
        upload_path = os.path.join(app.config["UPLOADS_DIR"], uploaded_file.filename)
        uploaded_file.save(upload_path)

        # ---- Call the appropriate converter ----
        if conversion_type == "image-to-text":
            result = image_to_text(upload_path)

        elif conversion_type == "audio-to-text":
            result = audio_to_text(upload_path)

        elif conversion_type == "video-to-audio":
            output_audio = os.path.join(app.config["RESULTS_DIR"], "extracted_audio.wav")
            result = video_to_audio(upload_path, output_audio)

        elif conversion_type == "video-to-text":
            result = video_to_text(upload_path)

        elif conversion_type == "video-to-images":
            output_dir = os.path.join(app.config["RESULTS_DIR"], "frames")
            result = video_to_images(upload_path, output_dir)

        else:
            return jsonify({
                "success": False,
                "error": f"Unknown conversion type: '{conversion_type}'.",
            }), 400

        # ---- If text result, save to requested format ----
        if result.get("success") and "text" in result and result["text"]:
            file_path = _save_text_result(
                result["text"], output_format, app.config["RESULTS_DIR"]
            )
            if file_path:
                result["download_file"] = os.path.basename(file_path)

        # ---- If video-to-audio, set download file ----
        elif conversion_type == "video-to-audio" and result.get("success"):
            result["download_file"] = os.path.basename(result["audio_path"])

        # ---- If video-to-images, zip frames and set download file ----
        elif conversion_type == "video-to-images" and result.get("success"):
            from morph.utils.exporter import export_to_zip
            zip_path = os.path.join(app.config["RESULTS_DIR"], "extracted_frames.zip")
            zip_res = export_to_zip(result["frames"], zip_path)
            if zip_res["success"]:
                result["download_file"] = "extracted_frames.zip"
            
            # Convert absolute frame paths to relative paths for frontend display
            relative_frames = []
            for frame_path in result["frames"]:
                rel_path = os.path.relpath(frame_path, app.config["RESULTS_DIR"])
                relative_frames.append(rel_path)
            result["frames"] = relative_frames

        # Return the result as JSON
        return jsonify(result)

    @app.route("/api/download/<path:filename>")
    def api_download(filename):
        """
        Download a previously saved result file.

        Parameters:
            filename (str): Name of the file to download (supports paths).

        Returns:
            The file as a download, or a 404 error if not found.
        """
        # Build the full path to the file
        file_path = os.path.join(app.config["RESULTS_DIR"], filename)

        # Check that the file exists
        if not os.path.exists(file_path):
            return jsonify({"success": False, "error": "File not found."}), 404

        # Send the file to the user as a download
        return send_file(file_path, as_attachment=True)

    return app


def _save_text_result(text, output_format, results_dir):
    """
    Save text results to a file in the specified format.

    Parameters:
        text (str): The text to save.
        output_format (str): The format ('txt', 'csv', or 'json').
        results_dir (str): Directory to save the file in.

    Returns:
        str or None: Path to the saved file, or None if saving failed.
    """
    if output_format == "txt":
        file_path = os.path.join(results_dir, "scraped_text.txt")
        result = export_to_txt(text, file_path)
    elif output_format == "csv":
        file_path = os.path.join(results_dir, "scraped_text.csv")
        lines = text.split("\n")
        result = export_to_csv(lines, file_path, headers=["text"])
    elif output_format == "json":
        file_path = os.path.join(results_dir, "scraped_text.json")
        result = export_to_json({"text": text}, file_path)
    else:
        return None

    if result["success"]:
        return file_path
    return None
