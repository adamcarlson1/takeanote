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


## Requirements
Ensure you have the following dependencies installed before running the application:
- [OpenAI kEY](https://openai.com/index/openai-api/) - Open API Key for Calls
- [Flask](https://flask.palletsprojects.com/) - Web framework for Python
- [OpenAI](https://pypi.org/project/openai/) - API for AI models
- [Whisper](https://github.com/openai/whisper) - Speech-to-text processing
- [Transformers](https://huggingface.co/docs/transformers/) - NLP tasks
- [Torch](https://pytorch.org/) - Deep learning framework
- [OS](https://docs.python.org/3/library/os.html) - Standard Python module for system operations
- [Logging](https://docs.python.org/3/library/logging.html) - Logging support
- [JSON](https://docs.python.org/3/library/json.html) - Parsing and handling JSON data
- [re (Regex)](https://docs.python.org/3/library/re.html) - Regular expressions
- [dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
- [pypandoc](https://pypi.org/project/pypandoc/) - Convert documents using Pandoc

### To install all dependencies, 

**run:**
```bash
pip install Flask openai whisper transformers torch python-dotenv pypandoc
```

## File Structure
```
├── app/
│   ├── __init__.py         # Initializes the Flask (or FastAPI) application
│   ├── routes.py           # Defines routes/endpoints for uploading videos and displaying results
│   ├── transcription.py    # Handles video-to-text transcription (e.g., using OpenAI Whisper)
│   ├── summarization.py    # Contains functions to create lecture notes & bullet points (using NLP models)
│   ├── .env                # API keys & config (ignored in Git)
│   └── quiz_generator.py   # Generates active learning questions based on the text
├── static/                 # Frontend assets (CSS, JavaScript, images)
│   ├── css/
│   └── js/
├── templates/              # HTML templates for rendering pages
│   ├── index.html          # Homepage with upload form
│   ├── results.html        # Page to display notes and bullet points
│   └── quiz.html           # Page to display generated quiz questions
├── data/
│   ├── uploads/            # Directory to store uploaded lecture videos
│   ├── transcripts/        # Directory to store transcripts by Whisper
│   ├── summaries/          # Directory to store summaries made from transcripts
│   ├── session_files/      # Directory to store metada of lecture videos
│   └── quiz/               # Directory to store quizzes made from summaries   
├── requirements.txt        # List of required Python packages
└── run.py                  # Entry point to run the application
```

# How to use the Application 

1. Setup Environment Variables
    -  Create or update the `.env` file in the app directory and **add** your 
    OpenAI API key. `OPENAI_API_KEY=your-api-key-here`

2. In the command line terminal to start the application: `python3 run.py`


### Authors

Daniel Folino 
Alberto Espinosa 
Adam Carlson