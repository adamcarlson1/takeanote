from flask import Blueprint, render_template, request, current_app, redirect, flash, url_for, session
import os
from .transcription import transcribe_video
from .summarization import TranscriptSummarizer
from .quiz_generator import generate_quiz
import sys  # Debug prints

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    print('Entered index')
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
        
        # Transcribe the video
        transcription = transcribe_video(video_path)
        
        # Check for transcription errors
        if "failed" in transcription.lower():
            flash("Error during transcription: " + transcription, "error")
            session['transcription'] = transcription
            session['notes'] = {"detailed_notes": "No summary available due to transcription error."}
            session['quiz'] = []
            return redirect(url_for('main.results'))
        
        # If transcription succeeded, generate summary and quiz
        summarizer = TranscriptSummarizer()
        cleaned_transcript = summarizer.clean_transcript(transcription)
        summary_text = summarizer.generate_summary(cleaned_transcript)
        notes = {"detailed_notes": summary_text}
        quiz = generate_quiz(notes["detailed_notes"])

        session['transcription'] = transcription
        session['notes'] = notes
        session['quiz'] = quiz

        print("✅ Redirecting to results page...", file=sys.stderr)
        return redirect(url_for('main.results'))

    return render_template('index.html')


@bp.route('/results', methods=['GET'])
def results():
    print('Entered results')
    transcription = session.get('transcription')
    notes = session.get('notes')
    quiz = session.get('quiz')

    if not transcription:
        flash("No results available. Please upload a video first.", "error")
        return redirect(url_for('main.index'))

    return render_template('results.html', transcription=transcription, notes=notes, quiz=quiz)


@bp.route('/quiz', methods=['GET'])
def quiz_page():
    print('Entered quiz')
    quiz = session.get('quiz', [])
    return render_template('quiz.html', quiz=quiz)
