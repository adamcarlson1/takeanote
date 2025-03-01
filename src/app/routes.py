from flask import Blueprint, render_template, request, current_app, redirect, flash, url_for, session
import os
from .transcription import transcribe_video
from .summarization import generate_notes
from .quiz_generator import generate_quiz
import sys  # Debugging prints

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files.get('video')
        if not video or video.filename == '':
            flash('No video file provided. Please select a video.', 'error')
            return redirect(request.url)

        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        video_path = os.path.join(upload_folder, video.filename)
        video.save(video_path)

        print("✅ Video uploaded successfully. Processing...", file=sys.stderr)

        # Dummy Processing
        transcription = transcribe_video(video_path)
        notes = generate_notes(transcription)
        quiz = generate_quiz(notes["detailed_notes"])

        session['transcription'] = transcription
        session['notes'] = notes
        session['quiz'] = quiz

        print("✅ Redirecting to results page...", file=sys.stderr)

        return redirect(url_for('main.results'))  # Ensure correct redirect

    return render_template('index.html')


@bp.route('/results', methods=['GET'])
def results():
    transcription = session.get('transcription')
    notes = session.get('notes')
    quiz = session.get('quiz')

    if not transcription:
        flash("No results available. Please upload a video first.", "error")
        return redirect(url_for('main.index'))

    return render_template('results.html', transcription=transcription, notes=notes, quiz=quiz)


@bp.route('/quiz', methods=['GET'])
def quiz_page():
    quiz = session.get('quiz', [])
    return render_template('quiz.html', quiz=quiz)

