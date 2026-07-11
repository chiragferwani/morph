"""
morph.utils.exporter - Functions for exporting data to various file formats.

This module handles saving scraped data into TXT, CSV, JSON files,
and creating ZIP archives of downloaded files.
"""

import os
import csv
import json
import zipfile


def export_to_txt(data, file_path):
    """
    Export text data to a plain .txt file.

    Parameters:
        data (str or list): The text to save. If a list is given,
            each item is written on a new line.
        file_path (str): Path where the .txt file will be saved.

    Returns:
        dict: Result with 'success' (bool), 'file_path' (str), 'error' (str or None).
    """
    try:
        # Make sure the directory exists
        _ensure_directory_exists(file_path)

        # Open the file for writing text
        with open(file_path, "w", encoding="utf-8") as file:

            # If data is a list, write each item on its own line
            if isinstance(data, list):
                for item in data:
                    file.write(str(item) + "\n")
            else:
                # If data is a string, write it directly
                file.write(str(data))

        return {"success": True, "file_path": file_path, "error": None}

    except PermissionError:
        return {
            "success": False,
            "file_path": None,
            "error": f"Permission denied: cannot write to '{file_path}'.",
        }

    except Exception as error:
        return {
            "success": False,
            "file_path": None,
            "error": f"Export to TXT failed: {str(error)}",
        }


def export_to_csv(data, file_path, headers=None):
    """
    Export data to a .csv file.

    Parameters:
        data (list): A list of rows. Each row can be:
            - A list/tuple of values (written as columns)
            - A dictionary (keys become column headers)
            - A string (written as a single-column row)
        file_path (str): Path where the .csv file will be saved.
        headers (list, optional): Column headers for the CSV file.

    Returns:
        dict: Result with 'success' (bool), 'file_path' (str), 'error' (str or None).
    """
    try:
        # Make sure the directory exists
        _ensure_directory_exists(file_path)

        with open(file_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            # Write the header row if provided
            if headers is not None:
                writer.writerow(headers)

            # If data is a list of dictionaries, handle them specially
            if len(data) > 0 and isinstance(data[0], dict):
                # Use the dictionary keys as headers if none provided
                if headers is None:
                    dict_headers = list(data[0].keys())
                    writer.writerow(dict_headers)

                # Write each dictionary as a row
                for row in data:
                    writer.writerow(list(row.values()))

            else:
                # Write each item as a row
                for row in data:
                    # If the row is a list or tuple, write its items as columns
                    if isinstance(row, (list, tuple)):
                        writer.writerow(row)
                    else:
                        # Otherwise, write it as a single-column row
                        writer.writerow([str(row)])

        return {"success": True, "file_path": file_path, "error": None}

    except PermissionError:
        return {
            "success": False,
            "file_path": None,
            "error": f"Permission denied: cannot write to '{file_path}'.",
        }

    except Exception as error:
        return {
            "success": False,
            "file_path": None,
            "error": f"Export to CSV failed: {str(error)}",
        }


def export_to_json(data, file_path):
    """
    Export data to a .json file.

    Parameters:
        data: Any JSON-serializable data (dict, list, string, etc.).
        file_path (str): Path where the .json file will be saved.

    Returns:
        dict: Result with 'success' (bool), 'file_path' (str), 'error' (str or None).
    """
    try:
        # Make sure the directory exists
        _ensure_directory_exists(file_path)

        with open(file_path, "w", encoding="utf-8") as file:
            # Write the data as formatted JSON (indent=2 makes it readable)
            json.dump(data, file, indent=2, ensure_ascii=False)

        return {"success": True, "file_path": file_path, "error": None}

    except PermissionError:
        return {
            "success": False,
            "file_path": None,
            "error": f"Permission denied: cannot write to '{file_path}'.",
        }

    except Exception as error:
        return {
            "success": False,
            "file_path": None,
            "error": f"Export to JSON failed: {str(error)}",
        }


def export_to_zip(file_paths, zip_path):
    """
    Create a ZIP archive containing the given files.

    Parameters:
        file_paths (list): List of file paths to include in the ZIP.
        zip_path (str): Path where the .zip file will be saved.

    Returns:
        dict: Result with 'success' (bool), 'file_path' (str), 'error' (str or None).
    """
    try:
        # Make sure the directory for the zip file exists
        _ensure_directory_exists(zip_path)

        # Create the ZIP file
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:

            # Add each file to the archive
            for path in file_paths:
                # Check that the file actually exists
                if os.path.exists(path):
                    # Use just the filename inside the zip (not the full path)
                    archive_name = os.path.basename(path)
                    zip_file.write(path, archive_name)

        return {"success": True, "file_path": zip_path, "error": None}

    except PermissionError:
        return {
            "success": False,
            "file_path": None,
            "error": f"Permission denied: cannot write to '{zip_path}'.",
        }

    except Exception as error:
        return {
            "success": False,
            "file_path": None,
            "error": f"Export to ZIP failed: {str(error)}",
        }


def _ensure_directory_exists(file_path):
    """
    Create the parent directory of a file if it doesn't exist yet.

    Parameters:
        file_path (str): The path to a file whose directory should exist.
    """
    # Get the directory part of the path
    directory = os.path.dirname(file_path)

    # Only create if there's a directory component and it doesn't exist
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
