"""
morph.converters.video_converter - Convert video files to audio, text, and images.

This module uses moviepy to process video files and extract:
    - Audio tracks (video_to_audio)
    - Text via speech recognition (video_to_text)
    - Frames as images (video_to_images)

Requirements:
    - moviepy (Python library for video editing)
    - ffmpeg (system package, needed by moviepy)
      Install with: sudo apt install ffmpeg (Linux)
                    brew install ffmpeg (macOS)
"""

import os

# Import frame capture interval from config
from morph.core.config import FRAME_CAPTURE_INTERVAL

# Try to import moviepy for video processing
try:
    # Try importing from moviepy v2.x first
    from moviepy import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    try:
        # Fall back to moviepy v1.x
        from moviepy.editor import VideoFileClip
        MOVIEPY_AVAILABLE = True
    except ImportError:
        MOVIEPY_AVAILABLE = False

# Import our audio converter for the video_to_text function
from morph.converters.audio_converter import audio_to_text


def video_to_audio(video_path, output_path=None):
    """
    Extract the audio track from a video file.

    This function:
        1. Checks that moviepy is installed
        2. Opens the video file
        3. Extracts just the audio portion
        4. Saves it as a WAV file

    Parameters:
        video_path (str): Path to the video file.
        output_path (str, optional): Where to save the audio file.
            If not provided, saves next to the video with a .wav extension.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the extraction succeeded.
            - 'video_path' (str): The input video path.
            - 'audio_path' (str or None): Path to the extracted audio.
            - 'error' (str or None): Error message if extraction failed.
    """

    # ---- Step 1: Check that moviepy is installed ----
    if not MOVIEPY_AVAILABLE:
        return {
            "success": False,
            "video_path": video_path,
            "audio_path": None,
            "error": (
                "moviepy library not installed. "
                "Please install with: pip install moviepy"
            ),
        }

    # ---- Step 2: Check that the video file exists ----
    if not os.path.exists(video_path):
        return {
            "success": False,
            "video_path": video_path,
            "audio_path": None,
            "error": f"Video file not found: '{video_path}'",
        }

    try:
        # ---- Step 3: Generate output path if not provided ----
        if output_path is None:
            # Replace the video extension with .wav
            base_name = os.path.splitext(video_path)[0]
            output_path = base_name + ".wav"

        # ---- Step 4: Open the video file ----
        video = VideoFileClip(video_path)

        # ---- Step 5: Check that the video has audio ----
        if video.audio is None:
            video.close()
            return {
                "success": False,
                "video_path": video_path,
                "audio_path": None,
                "error": "This video has no audio track.",
            }

        # ---- Step 6: Extract and save the audio ----
        video.audio.write_audiofile(output_path)

        # ---- Step 7: Clean up ----
        video.close()

        return {
            "success": True,
            "video_path": video_path,
            "audio_path": output_path,
            "error": None,
        }

    except Exception as error:
        return {
            "success": False,
            "video_path": video_path,
            "audio_path": None,
            "error": f"Video to audio conversion failed: {str(error)}",
        }


def video_to_text(video_path):
    """
    Extract text from a video's audio using speech recognition.

    This is a two-step process:
        1. Extract the audio from the video
        2. Run speech recognition on the audio

    Parameters:
        video_path (str): Path to the video file.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the conversion succeeded.
            - 'video_path' (str): The input video path.
            - 'text' (str): The transcribed text.
            - 'word_count' (int): Number of words found.
            - 'error' (str or None): Error message if conversion failed.
    """

    # ---- Step 1: Extract audio from the video ----
    audio_result = video_to_audio(video_path)

    # Check if audio extraction succeeded
    if not audio_result["success"]:
        return {
            "success": False,
            "video_path": video_path,
            "text": "",
            "word_count": 0,
            "error": f"Could not extract audio: {audio_result['error']}",
        }

    # ---- Step 2: Convert the extracted audio to text ----
    text_result = audio_to_text(audio_result["audio_path"])

    # ---- Step 3: Clean up the temporary audio file ----
    try:
        if os.path.exists(audio_result["audio_path"]):
            os.remove(audio_result["audio_path"])
    except OSError:
        # It's okay if cleanup fails, the conversion still succeeded
        pass

    # ---- Step 4: Return the result ----
    return {
        "success": text_result["success"],
        "video_path": video_path,
        "text": text_result["text"],
        "word_count": text_result["word_count"],
        "error": text_result["error"],
    }


def video_to_images(video_path, output_dir=None, interval=None):
    """
    Extract frames (images) from a video at regular intervals.

    This function captures a screenshot from the video every N seconds
    and saves each frame as a PNG image.

    Parameters:
        video_path (str): Path to the video file.
        output_dir (str, optional): Directory to save the extracted frames.
            If not provided, creates a folder next to the video file.
        interval (float, optional): Time in seconds between frame captures.
            Defaults to FRAME_CAPTURE_INTERVAL from config (1.0 second).

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the extraction succeeded.
            - 'video_path' (str): The input video path.
            - 'frames' (list): List of paths to saved frame images.
            - 'count' (int): Number of frames extracted.
            - 'error' (str or None): Error message if extraction failed.
    """

    # ---- Step 1: Check that moviepy is installed ----
    if not MOVIEPY_AVAILABLE:
        return {
            "success": False,
            "video_path": video_path,
            "frames": [],
            "count": 0,
            "error": (
                "moviepy library not installed. "
                "Please install with: pip install moviepy"
            ),
        }

    # ---- Step 2: Check that the video file exists ----
    if not os.path.exists(video_path):
        return {
            "success": False,
            "video_path": video_path,
            "frames": [],
            "count": 0,
            "error": f"Video file not found: '{video_path}'",
        }

    try:
        # ---- Step 3: Set up output directory ----
        if output_dir is None:
            # Create a folder named like "video_frames" next to the video file
            base_name = os.path.splitext(video_path)[0]
            output_dir = base_name + "_frames"

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # ---- Step 4: Set the capture interval ----
        if interval is None:
            interval = FRAME_CAPTURE_INTERVAL

        # ---- Step 5: Open the video ----
        video = VideoFileClip(video_path)

        # Get the total duration of the video in seconds
        total_duration = video.duration

        # ---- Step 6: Capture frames at regular intervals ----
        saved_frames = []
        current_time = 0.0
        frame_number = 1

        while current_time < total_duration:
            # Create the filename for this frame
            frame_filename = f"frame_{frame_number:04d}.png"
            frame_path = os.path.join(output_dir, frame_filename)

            # Capture the frame at the current time position
            frame = video.get_frame(current_time)

            # Save the frame as an image using PIL
            from PIL import Image
            image = Image.fromarray(frame)
            image.save(frame_path)

            # Add the path to our list
            saved_frames.append(frame_path)

            # Move to the next time position
            current_time = current_time + interval
            frame_number = frame_number + 1

        # ---- Step 7: Clean up ----
        video.close()

        return {
            "success": True,
            "video_path": video_path,
            "frames": saved_frames,
            "count": len(saved_frames),
            "error": None,
        }

    except Exception as error:
        return {
            "success": False,
            "video_path": video_path,
            "frames": [],
            "count": 0,
            "error": f"Frame extraction failed: {str(error)}",
        }
