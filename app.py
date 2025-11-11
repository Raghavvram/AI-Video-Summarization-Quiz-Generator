import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import time
from transcription import process_video_transcription
from summarization import summarize_transcript, extract_key_concepts
from quiz_generator import generate_quiz, save_quiz

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app.route('/upload', methods=['POST'])
def upload_video():
    """Upload video file."""
    try:
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400

        file = request.files['video']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": f"File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}"}), 400

        filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)

        return jsonify({
            "message": "Video uploaded successfully",
            "filename": filename,
            "filepath": filepath
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcribe video to text."""
    try:
        data = request.get_json()
        filepath = data.get('filepath')

        if not filepath or not os.path.exists(filepath):
            return jsonify({"error": "Video file not found"}), 404

        # Process transcription
        transcript_text, segments = process_video_transcription(filepath)

        # Save transcript
        transcript_filename = os.path.join(OUTPUT_FOLDER, f"transcript_{int(time.time())}.txt")
        with open(transcript_filename, 'w', encoding='utf-8') as f:
            f.write(transcript_text)

        return jsonify({
            "message": "Transcription completed",
            "transcript": transcript_text,
            "transcript_file": transcript_filename,
            "segments": segments
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    """Generate summary from transcript."""
    try:
        data = request.get_json()
        transcript = data.get('transcript')
        length = data.get('length', 'medium')  # short, medium, long

        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400

        # Generate summary
        summary = summarize_transcript(transcript, length)

        # Extract key concepts
        key_concepts = extract_key_concepts(transcript)

        return jsonify({
            "message": "Summary generated successfully",
            "summary": summary,
            "key_concepts": key_concepts
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-quiz', methods=['POST'])
def create_quiz():
    """Generate quiz from transcript."""
    try:
        data = request.get_json()
        transcript = data.get('transcript')
        num_questions = data.get('num_questions', 5)
        difficulty = data.get('difficulty', 'medium')  # easy, medium, hard
        question_type = data.get('question_type', 'mcq')  # mcq, true_false, mixed

        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400

        # Generate quiz
        quiz_data = generate_quiz(transcript, num_questions, difficulty, question_type)

        # Save quiz
        quiz_filename = os.path.join(OUTPUT_FOLDER, f"quiz_{int(time.time())}.json")
        save_quiz(quiz_data, quiz_filename)

        return jsonify({
            "message": "Quiz generated successfully",
            "quiz": quiz_data,
            "quiz_file": quiz_filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process-all', methods=['POST'])
def process_all():
    """Complete pipeline: upload -> transcribe -> summarize -> generate quiz."""
    try:
        # Check if video file is provided
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400

        file = request.files['video']

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Get parameters
        num_questions = int(request.form.get('num_questions', 5))
        difficulty = request.form.get('difficulty', 'medium')
        summary_length = request.form.get('summary_length', 'medium')

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Step 1: Transcribe
        transcript_text, segments = process_video_transcription(filepath)

        # Step 2: Summarize
        summary = summarize_transcript(transcript_text, summary_length)
        key_concepts = extract_key_concepts(transcript_text)

        # Step 3: Generate quiz
        quiz_data = generate_quiz(transcript_text, num_questions, difficulty)

        # Save outputs
        transcript_file = os.path.join(OUTPUT_FOLDER, f"transcript_{timestamp}.txt")
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript_text)

        quiz_file = os.path.join(OUTPUT_FOLDER, f"quiz_{timestamp}.json")
        save_quiz(quiz_data, quiz_file)

        return jsonify({
            "message": "Processing completed successfully",
            "transcript": transcript_text,
            "summary": summary,
            "key_concepts": key_concepts,
            "quiz": quiz_data,
            "files": {
                "transcript": transcript_file,
                "quiz": quiz_file
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask API server...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Output folder: {OUTPUT_FOLDER}")
    app.run(debug=True, host='0.0.0.0', port=5000)
