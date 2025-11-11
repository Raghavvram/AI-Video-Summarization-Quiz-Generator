# AI Video Summarization & Quiz Generator

An intelligent educational tool that automatically transcribes videos, generates comprehensive summaries, and creates interactive quizzes using OpenAI's Whisper and GPT-4 models.

## 🌟 Features

- **Video Transcription**: Automatically transcribe video content using OpenAI Whisper
- **Smart Summarization**: Generate concise summaries with key concepts extraction
- **Quiz Generation**: Create multiple-choice questions with varying difficulty levels
- **Interactive UI**: User-friendly Streamlit interface
- **RESTful API**: Flask-based backend for flexible integration
- **Download Options**: Export transcripts, summaries, and quizzes

## 🛠️ Technology Stack

- **Backend**: Python, Flask, OpenAI API
- **Frontend**: Streamlit
- **AI Models**: Whisper (transcription), GPT-4 (summarization & quiz generation)
- **Video Processing**: MoviePy
- **LLM Framework**: LangChain

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key
- FFmpeg (for video processing)

## 🚀 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd video-quiz-ai
```

### 2. Create virtual environment
```bash
python -m venv venv

# On Windows
venv\\Scripts\\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Create necessary folders
```bash
mkdir uploads outputs
```

## 💻 Usage

### Running the Application

#### Step 1: Start the Flask API Server
```bash
python app.py
```
The API will be available at `http://localhost:5000`

#### Step 2: Launch the Streamlit Frontend (in a new terminal)
```bash
streamlit run streamlit_app.py
```
The web interface will open at `http://localhost:8501`

### Using the Web Interface

1. **Upload Video**: Click "Browse files" and select your educational video
2. **Configure Settings**:
   - Number of quiz questions (3-10)
   - Difficulty level (Easy/Medium/Hard)
   - Summary length (Short/Medium/Long)
3. **Process**: Click "🚀 Process Video" button
4. **View Results**: Navigate through tabs to see transcript, summary, and quiz
5. **Take Quiz**: Answer questions and submit to see your score
6. **Download**: Export any output using download buttons

### Using the API Directly

#### Health Check
```bash
curl http://localhost:5000/health
```

#### Upload Video
```bash
curl -X POST -F "video=@path/to/video.mp4" http://localhost:5000/upload
```

#### Complete Processing Pipeline
```bash
curl -X POST \\
  -F "video=@path/to/video.mp4" \\
  -F "num_questions=5" \\
  -F "difficulty=medium" \\
  -F "summary_length=medium" \\
  http://localhost:5000/process-all
```

## 📁 Project Structure

```
video-quiz-ai/
│
├── app.py                      # Flask API main application
├── transcription.py            # Video transcription module
├── summarization.py            # Summary generation module
├── quiz_generator.py           # Quiz generation module
├── streamlit_app.py            # Streamlit web interface
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .env                        # Environment variables (create this)
│
├── uploads/                    # Uploaded videos (auto-created)
├── outputs/                    # Generated files (auto-created)
│
└── README.md                   # This file
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t video-quiz-ai .
```

### Run Container
```bash
docker run -p 5000:5000 -p 8501:8501 \\
  -e OPENAI_API_KEY=your_key_here \\
  -v $(pwd)/uploads:/app/uploads \\
  -v $(pwd)/outputs:/app/outputs \\
  video-quiz-ai
```

## ⚙️ Configuration

Edit `config.py` to customize:
- File size limits
- Supported video formats
- Default quiz parameters
- API settings

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/upload` | POST | Upload video file |
| `/transcribe` | POST | Transcribe video |
| `/summarize` | POST | Generate summary |
| `/generate-quiz` | POST | Create quiz |
| `/process-all` | POST | Complete pipeline |

## 🔍 Example Output

### Transcript
```
Artificial intelligence has revolutionized many industries...
```

### Summary
```
This video covers the fundamentals of artificial intelligence, 
including machine learning, deep learning, and their applications...
```

### Quiz
```json
{
  "quiz_title": "AI Fundamentals Quiz",
  "questions": [
    {
      "question_number": 1,
      "question_text": "What is machine learning?",
      "options": {
        "A": "A type of computer hardware",
        "B": "A subset of AI that learns from data",
        "C": "A programming language",
        "D": "A type of algorithm"
      },
      "correct_answer": "B",
      "explanation": "Machine learning is a subset of AI..."
    }
  ]
}
```

## 🛡️ Error Handling

- Maximum file size: 100MB
- Supported formats: MP4, AVI, MOV, MKV, WEBM
- Audio files > 25MB are automatically chunked
- API rate limits are handled gracefully

## 💰 Cost Considerations

This project uses OpenAI's paid APIs:
- **Whisper API**: ~$0.006 per minute of audio
- **GPT-4 API**: Variable based on token usage

Estimate: Processing a 10-minute video costs approximately $0.06-0.15

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### Common Issues

1. **"Could not connect to API"**
   - Ensure Flask server is running on port 5000
   - Check if port is already in use

2. **"File too large"**
   - Video must be under 100MB
   - Consider compressing the video

3. **"OpenAI API error"**
   - Verify your API key is valid
   - Check your OpenAI account has sufficient credits

4. **"FFmpeg not found"**
   - Install FFmpeg: `brew install ffmpeg` (macOS) or download from ffmpeg.org

## 📧 Support

For issues and questions, please open an issue on GitHub.

## 🎓 Use Cases

- **Education**: Create study materials from lecture videos
- **Corporate Training**: Generate assessments from training videos
- **Content Creation**: Summarize and test understanding of video content
- **E-Learning Platforms**: Automate quiz creation for courses

---

**Built with ❤️ using OpenAI APIs, Flask, and Streamlit**
