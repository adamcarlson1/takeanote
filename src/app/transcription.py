import os
import subprocess
import whisper
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe_video(video_path: str) -> str:
    """
    Transcribes the video at video_path using OpenAI's Whisper model.
    1. Convert the video to a WAV audio file using ffmpeg.
    2. Load the Whisper model (using the "base" model).
    3. Transcribe the extracted audio.
    4. Delete the temporary audio file.
    Returns the transcribed text or an error message if transcription fails.
    """
    try:
        # Construct a temporary audio file path by replacing the video extension with .wav
        audio_path = os.path.splitext(video_path)[0] + ".wav"
        
        # Convert the video to audio using ffmpeg
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-ac", "1", "-ar", "16000", audio_path],
            check=True
        )
        logger.info("Audio extracted to %s", audio_path)
        
        # Load the Whisper model; using the "base" model for speed/accuracy trade-off.
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcript = result.get("text", "")
        logger.info("Transcription completed successfully.")
        
        # Remove the temporary audio file
        os.remove(audio_path)
        
        return transcript
    except FileNotFoundError:
        logger.error("ffmpeg not found. Please install ffmpeg and ensure it's in your PATH.")
        return "Transcription failed: ffmpeg not found."
    except Exception as e:
        logger.error("Error transcribing video: %s", e, exc_info=True)
        return "Transcription failed."
