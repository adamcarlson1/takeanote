lecture_app/
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
