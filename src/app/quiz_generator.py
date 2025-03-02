import os
import logging
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuizGenerator:
    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 1000):
        """
        Initializes the quiz generator using OpenAI's model.
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OPENAI_API_KEY environment variable not set!")
            raise ValueError("Please set the OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)

    def generate_quiz(self, summary_text: str) -> list:
        """
        Generates a structured multiple-choice quiz based on the lecture summary.
        The quiz should contain 3 questions. Each question will have 4 options (A, B, C, D).
        The output is expected strictly as JSON in the following format:
        
        [
          {
            "question": "Question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "A"  // Correct option letter (this field is optional for display)
          },
          ...
        ]
        
        Args:
            summary_text (str): The lecture summary text.
        
        Returns:
            list: A list of dictionaries representing the quiz questions.
        """
        prompt = (
            "Based on the following lecture summary, generate a multiple-choice quiz with 3 questions. "
            "Each question should have 4 options labeled A, B, C, and D. "
            "Output the quiz in strict JSON format exactly as follows:\n\n"
            "[\n"
            "  {\n"
            "    \"question\": \"<question text>\",\n"
            "    \"options\": [\"<option A>\", \"<option B>\", \"<option C>\", \"<option D>\"],\n"
            "    \"answer\": \"<correct option letter>\"\n"
            "  },\n"
            "  ...\n"
            "]\n\n"
            "Lecture Summary:\n" + summary_text
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            quiz_json = response.choices[0].message.content.strip()
            # Attempt to parse the JSON output
            quiz_data = json.loads(quiz_json)
            logger.info("Quiz generated successfully.")
            return quiz_data
        except Exception as e:
            logger.error("Error generating quiz: %s", e, exc_info=True)
            return [{
                "question": "Quiz generation failed. Please try again.",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "A"
            }]

# Expose a top-level function for convenience
def generate_quiz(summary_text: str) -> list:
    generator = QuizGenerator()
    return generator.generate_quiz(summary_text)

if __name__ == "__main__":
    # For testing purposes: load a sample summary and generate a quiz
    sample_summary = (
        "In this lecture, key topics included the fundamentals of machine learning, "
        "the importance of data preprocessing, and an overview of various algorithms "
        "such as decision trees and neural networks. Practical examples were provided "
        "to illustrate how these concepts can be applied in real-world scenarios."
    )
    quiz = generate_quiz(sample_summary)
    print("Generated Quiz:")
    print(json.dumps(quiz, indent=2))
