"""
morph.converters.audio_converter - Convert audio files to text using speech recognition.

This module uses the SpeechRecognition library to transcribe audio files
(MP3, WAV) into text. It uses Google's free Web Speech API by default.

Requirements:
    - SpeechRecognition (Python library)
    - pydub (for MP3 to WAV conversion)
    - ffmpeg (system package, needed by pydub for MP3 support)
      Install with: sudo apt install ffmpeg (Linux)
                    brew install ffmpeg (macOS)
"""

import os
import tempfile

# Try to import required libraries, with clear error messages if missing
try:
    # 'speech_recognition' provides easy access to speech-to-text engines
    import speech_recognition as sr

    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    # 'pydub' is used to convert MP3 files to WAV format
    # (speech_recognition works best with WAV files)
    from pydub import AudioSegment

    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


def audio_to_text(audio_path):
    """
    Convert an audio file to text using speech recognition.

    This function:
        1. Checks that required libraries are installed
        2. Converts MP3 to WAV if needed (speech recognition needs WAV)
        3. Loads the audio file
        4. Sends it to Google's speech recognition API
        5. Returns the transcribed text

    Parameters:
        audio_path (str): Path to the audio file (MP3 or WAV).

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): Whether the conversion succeeded.
            - 'audio_path' (str): The path to the audio file processed.
            - 'text' (str): The transcribed text.
            - 'word_count' (int): Number of words in the transcription.
            - 'error' (str or None): Error message if conversion failed.
    """

    # ---- Step 1: Check that speech_recognition is installed ----
    if not SPEECH_RECOGNITION_AVAILABLE:
        return {
            "success": False,
            "audio_path": audio_path,
            "text": "",
            "word_count": 0,
            "error": (
                "SpeechRecognition library not installed. "
                "Please install with: pip install SpeechRecognition"
            ),
        }

    # ---- Step 2: Check that the audio file exists ----
    if not os.path.exists(audio_path):
        return {
            "success": False,
            "audio_path": audio_path,
            "text": "",
            "word_count": 0,
            "error": f"Audio file not found: '{audio_path}'",
        }

    try:
        # ---- Step 3: Convert to WAV if the file is MP3 ----
        wav_path = _ensure_wav_format(audio_path)

        # ---- Step 4: Create a recognizer instance ----
        recognizer = sr.Recognizer()

        # ---- Step 5: Load the audio file ----
        with sr.AudioFile(wav_path) as audio_source:
            # Read the entire audio file
            audio_data = recognizer.record(audio_source)

        # ---- Step 6: Send to Google's speech recognition ----
        # This uses Google's free Web Speech API (requires internet)
        transcribed_text = recognizer.recognize_google(audio_data)

        # ---- Step 7: Count words ----
        word_count = len(transcribed_text.split()) if transcribed_text else 0

        # ---- Step 8: Clean up temporary WAV file if we created one ----
        if wav_path != audio_path and os.path.exists(wav_path):
            os.remove(wav_path)

        return {
            "success": True,
            "audio_path": audio_path,
            "text": transcribed_text,
            "word_count": word_count,
            "error": None,
        }

    except sr.UnknownValueError:
        return {
            "success": False,
            "audio_path": audio_path,
            "text": "",
            "word_count": 0,
            "error": "Could not understand the audio. The speech may be unclear.",
        }

    except sr.RequestError as error:
        return {
            "success": False,
            "audio_path": audio_path,
            "text": "",
            "word_count": 0,
            "error": f"Speech recognition API error: {str(error)}. Check your internet.",
        }

    except Exception as error:
        return {
            "success": False,
            "audio_path": audio_path,
            "text": "",
            "word_count": 0,
            "error": f"Audio to text conversion failed: {str(error)}",
        }


def _ensure_wav_format(audio_path):
    """
    Convert an audio file to WAV format if it's not already WAV.

    The speech_recognition library works best with WAV files,
    so we convert MP3 and other formats to WAV first.

    Parameters:
        audio_path (str): Path to the original audio file.

    Returns:
        str: Path to the WAV file (may be the original if already WAV).
    """
    # Get the file extension (lowercase)
    file_extension = os.path.splitext(audio_path)[1].lower()

    # If it's already a WAV file, no conversion needed
    if file_extension == ".wav":
        return audio_path

    # Check that pydub is available for conversion
    if not PYDUB_AVAILABLE:
        # If pydub isn't installed, try using the file as-is
        return audio_path

    # Convert the audio to WAV using pydub
    # This creates a temporary WAV file
    audio = AudioSegment.from_file(audio_path)

    # Create a temporary file for the WAV output
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_wav_path = temp_wav.name
    temp_wav.close()

    # Export as WAV
    audio.export(temp_wav_path, format="wav")

    return temp_wav_path
