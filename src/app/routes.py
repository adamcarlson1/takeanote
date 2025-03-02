import os
from flask import Blueprint, render_template, request, current_app, redirect, flash, url_for, session
from .transcription import AudioTranscriber  # Your transcription class
from .summarization import TranscriptSummarizer  # Your summarization class
from .quiz_generator import generate_quiz  # Top-level function from quiz_generator
import sys

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    print('Entered index')
    if request.method == 'POST':
        video = request.files.get('video')
        if not video or video.filename == '':
            flash('No video file provided. Please select a video.', 'error')
            return redirect(request.url)

        # Save the uploaded video file
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        video_path = os.path.join(upload_folder, video.filename)
        video.save(video_path)
        print("✅ Video uploaded successfully. Processing...", file=sys.stderr)

        # Process transcription: transcribe the video and save the transcript
        transcriber = AudioTranscriber()
        transcript_path = transcriber.process_audio(video_path)

        # Process summarization: clean, summarize, and save the transcript summary
        summarizer = TranscriptSummarizer()
        summary_files = summarizer.process_transcript(transcript_path)

        # Read the transcript from the saved transcript file
        try:
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcription = f.read()
        except Exception as e:
            transcription = "Transcription could not be read."
            print(f"Error reading transcript: {e}", file=sys.stderr)

        # Read the summary from the saved summary text file (now in the quiz folder)
        try:
            with open(summary_files['txt'], "r", encoding="utf-8") as f:
                summary_text = f.read()
        except Exception as e:
            summary_text = "Summary could not be read."
            print(f"Error reading summary: {e}", file=sys.stderr)

        notes = {"detailed_notes": summary_text}

        # Generate a dynamic quiz based on the summary text
        quiz = generate_quiz(summary_text)

        # Save all results in the session
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
