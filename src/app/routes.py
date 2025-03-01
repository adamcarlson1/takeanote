# app/routes.py
from flask import Blueprint, render_template, request, current_app
import os
from app.transcription import transcribe_video
from app.summarization import generate_notes
from app.quiz_generator import generate_quiz

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    transcription, notes, quiz = None, None, None

    if request.method == 'POST':
        video = request.files['video']
        if video:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            video_path = os.path.join(upload_folder, video.filename)
            video.save(video_path)

            # Process video: Transcribe -> Summarize -> Generate Quiz
            transcription = transcribe_video(video_path)
            notes = generate_notes(transcription)
            quiz = generate_quiz(notes["detailed_notes"])

    return render_template('index.html', transcription=transcription, notes=notes, quiz=quiz)
