# Take a Note
App idea for CU Hackathon 11: Take a note

A web application that allows students to upload their zoom recordings, and creates detailed summaries, practice quizzes, audio files of the summaries, and slide presentations of them. 

## User interaction: 
1. User uploads video recordings
    - Create a transcript from the video file (Speech to text API) 
        - Ensure the trascript is corrected for misspellings, or incomplete sentences due to poor audio.

    - From the transcript, create a detailed summary that includes. The summary in .txt and .docx format. The summary should include
        - Example problems (if possible)
        - Key definitions and their definitions (autocomplete transcript) 

    - From Summary txt file: 
        - create an audio file for it (TTS API), 
        - a slide presentation (Slides API), 
        - quiz or example problems (GPT API)

2. User downloads: Summary file, Audio summary file, Quiz file, and presentation file.


## Code Structure

```lecture_app/
├── app/
│   ├── __init__.py         # Initializes the Flask (or FastAPI) application
│   ├── routes.py           # Defines routes/endpoints for uploading videos and displaying results
│   ├── transcription.py    # Handles video-to-text transcription (e.g., using OpenAI Whisper)
│   ├── summarization.py    # Contains functions to create lecture notes & bullet points (using NLP models)
│   └── quiz_generator.py   # Generates active learning questions based on the text
├── static/                 # Frontend assets (CSS, JavaScript, images)
│   ├── css/
│   └── js/
├── templates/              # HTML templates for rendering pages
│   ├── index.html          # Homepage with upload form
│   ├── results.html        # Page to display notes and bullet points
│   └── quiz.html           # Page to display generated quiz questions
├── data/
│   └── uploads/            # Directory to store uploaded lecture videos
├── requirements.txt        # List of required Python packages
└── run.py                  # Entry point to run the application
```
