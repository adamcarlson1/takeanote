import os
import logging
import glob
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioTranscriber:
    def __init__(self, model: str = "whisper-1"):
        """
        Initializes the transcription class using OpenAI's Whisper-1 model.
        """
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            logger.error("OPENAI_API_KEY environment variable not set!")
            raise ValueError(
                "Please set the OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)

    def transcribe_audio(self, audio_file: str) -> str:
        """
        Transcribes an audio file using OpenAI's Whisper model.

        Args:
            audio_file (str): Path to the audio file.

        Returns:
            str: Transcription of the audio.
        """
        logger.info(f"Processing audio file: {audio_file}")

        try:
            with open(audio_file, "rb") as file:
                response = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=file,
                    response_format="text"  # Can also use "json" if needed
                )
            transcript_text = response.strip()

            logger.info("Transcription successful.")
            return transcript_text
        except Exception as e:
            logger.error("Error during transcription: %s", e, exc_info=True)
            return "Transcription failed."

    def save_transcript(self, transcript_text: str):
        """
        Saves the transcript to ./../data/transcripts/raw_transcript.txt
        """
        save_dir = os.path.abspath(os.path.join(
            os.getcwd(), "./../data/transcripts/"))

        # Ensure directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Save the transcript
        transcript_file = os.path.join(save_dir, "raw_transcript.txt")
        with open(transcript_file, "w", encoding="utf-8") as txt_file:
            txt_file.write(transcript_text)

        logger.info(f"Transcript saved at: {transcript_file}")
        return transcript_file

    def process_audio(self, audio_file: str):
        """
        Transcribes audio and saves the transcript.
        """
        transcript_text = self.transcribe_audio(audio_file)
        transcript_path = self.save_transcript(transcript_text)
        return transcript_path


if __name__ == "__main__":
    # Dynamically determine the uploads folder path
    uploads_folder = os.path.abspath(os.path.join(os.getcwd(), "./../data/uploads/"))
    
    # Find all MP4 files in the uploads folder
    mp4_files = glob.glob(os.path.join(uploads_folder, "*.mp4"))
    
    if not mp4_files:
        print("No MP4 files found in the uploads folder.")
    else:
        # Get the most recently modified MP4 file
        latest_video = max(mp4_files, key=os.path.getmtime)
        print(f"Latest video found: {latest_video}")

        # Create an instance of the AudioTranscriber and process the audio
        transcriber = AudioTranscriber()
        transcript_file = transcriber.process_audio(latest_video)
        print(f"Transcript saved to: {transcript_file}")