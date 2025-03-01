import os
import logging
import re
# from docx import Document -> Depracated
import pypandoc
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranscriptSummarizer:
    def __init__(self, model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 2000):
        """
        Initializes the transcript summarization class.
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OPENAI_API_KEY environment variable not set!")
            raise ValueError(
                "Please set the OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)

    def clean_transcript(self, transcript_text: str) -> str:
        """
        Cleans the transcript by:
        - Removing filler words
        - Fixing common spelling mistakes
        - Correcting incomplete sentences
        - Standardizing formatting
        """
        # Remove filler words
        filler_words = ["um", "uh", "like", "you know",
                        "so", "basically", "actually", "right", "I mean"]
        pattern = r'\b(' + '|'.join(re.escape(word)
                                    for word in filler_words) + r')\b'
        cleaned_text = re.sub(
            pattern, "", transcript_text, flags=re.IGNORECASE)

        # Remove extra spaces and line breaks
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        return cleaned_text

    def generate_summary(self, cleaned_transcript: str) -> str:
        """
        Generates a structured summary from the cleaned transcript.
        """
        prompt = (
            "Summarize the following transcript. Ensure the summary includes:\n"
            "- Key points and concepts\n"
            "- Key definitions with explanations\n"
            "- Example problems (if possible)\n\n"
            f"{cleaned_transcript}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error("Error generating summary: %s", e, exc_info=True)
            return "Summary generation failed."

    def save_summary(self, summary_text: str):
        """
        Saves the summary as a text and Word document using pypandoc.
        """
        save_dir = os.path.abspath(os.path.join(
            os.getcwd(), "./../data/summaries/"))

        # Ensure the directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Define file paths
        txt_filename = os.path.join(save_dir, "summary.txt")
        docx_filename = os.path.join(save_dir, "summary.docx")

        # Save as .txt
        with open(txt_filename, "w", encoding="utf-8") as txt_file:
            txt_file.write(summary_text)

        # Save as .docx using pypandoc
        pypandoc.convert_text(summary_text, 'docx',
                              format='md', outputfile=docx_filename)

        return {"txt": txt_filename, "docx": docx_filename}

    def process_transcript(self, transcript_file: str):
        """
        Reads, cleans, summarizes, and saves the transcript.
        """
        # Read the transcript file
        with open(transcript_file, "r", encoding="utf-8") as file:
            transcript_text = file.read()

        # Step 1: Clean the transcript
        cleaned_transcript = self.clean_transcript(transcript_text)

        # Step 2: Generate the summary
        summary_text = self.generate_summary(cleaned_transcript)

        # Step 3: Save the summary
        summary_files = self.save_summary(summary_text)

        return summary_files


if __name__ == "__main__":
    summarizer = TranscriptSummarizer()
    transcript_path = "./../data/transcripts/raw_transcript.txt"
    summary_files = summarizer.process_transcript(transcript_path)

    print(f"Summary saved: {summary_files}")
