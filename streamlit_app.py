import streamlit as st
import requests
import json
import os
from pathlib import Path

# Configuration
API_URL = "http://localhost:5000"
TEMP_VIDEO_PATH = "temp_video.mp4"

# Page configuration
st.set_page_config(
    page_title="AI Video Quiz Generator",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .quiz-question {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .correct-answer {
        color: green;
        font-weight: bold;
    }
    .incorrect-answer {
        color: red;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables."""
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

def process_video_complete(video_file, num_questions, difficulty, summary_length):
    """Send video to API for complete processing."""
    try:
        files = {'video': video_file}
        data = {
            'num_questions': num_questions,
            'difficulty': difficulty,
            'summary_length': summary_length
        }

        with st.spinner('Processing video... This may take a few minutes.'):
            response = requests.post(
                f"{API_URL}/process-all",
                files=files,
                data=data,
                timeout=300
            )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            return None

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API. Make sure Flask server is running on port 5000.")
        return None
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        return None

def display_quiz(quiz_data):
    """Display quiz questions and collect answers."""
    st.markdown('<p class="sub-header">📝 Quiz Questions</p>', unsafe_allow_html=True)

    if not quiz_data or 'questions' not in quiz_data:
        st.warning("No quiz data available.")
        return

    st.write(f"**{quiz_data.get('quiz_title', 'Quiz')}**")
    st.write(f"Total Questions: {len(quiz_data['questions'])}")
    st.write("---")

    for idx, question in enumerate(quiz_data['questions']):
        with st.container():
            st.markdown(f"### Question {question.get('question_number', idx+1)}")
            st.write(question['question_text'])

            if question.get('question_type') == 'mcq' and 'options' in question:
                options_list = [f"{key}: {value}" for key, value in question['options'].items()]

                answer_key = f"q_{idx}"
                answer = st.radio(
                    "Select your answer:",
                    options_list,
                    key=answer_key,
                    disabled=st.session_state.quiz_submitted
                )

                if answer:
                    st.session_state.user_answers[idx] = answer[0]  # Store just the letter (A, B, C, D)

            # Show explanation if quiz is submitted
            if st.session_state.quiz_submitted:
                correct_answer = question.get('correct_answer')
                user_answer = st.session_state.user_answers.get(idx)

                if user_answer == correct_answer:
                    st.markdown(f'<p class="correct-answer">✓ Correct!</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="incorrect-answer">✗ Incorrect. Correct answer: {correct_answer}</p>', unsafe_allow_html=True)

                if 'explanation' in question:
                    st.info(f"**Explanation:** {question['explanation']}")

            st.write("---")

def calculate_score(quiz_data):
    """Calculate quiz score."""
    if not quiz_data or 'questions' not in quiz_data:
        return 0, 0

    correct = 0
    total = len(quiz_data['questions'])

    for idx, question in enumerate(quiz_data['questions']):
        if st.session_state.user_answers.get(idx) == question.get('correct_answer'):
            correct += 1

    return correct, total

def main():
    init_session_state()

    # Header
    st.markdown('<p class="main-header">🎥 AI Video Summarization & Quiz Generator</p>', unsafe_allow_html=True)
    st.markdown("### Transform educational videos into summaries and interactive quizzes using AI")

    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")

        num_questions = st.slider(
            "Number of quiz questions:",
            min_value=3,
            max_value=10,
            value=5,
            help="Select how many questions to generate"
        )

        difficulty = st.select_slider(
            "Quiz difficulty:",
            options=["easy", "medium", "hard"],
            value="medium",
            help="Select the difficulty level of quiz questions"
        )

        summary_length = st.select_slider(
            "Summary length:",
            options=["short", "medium", "long"],
            value="medium",
            help="Select the length of the summary"
        )

        st.write("---")
        st.info("📌 **How to use:**\n1. Upload a video file\n2. Configure settings\n3. Click 'Process Video'\n4. View results and take the quiz!")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📤 Upload Video")
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
            help="Upload an educational video (max 100MB)"
        )

    with col2:
        st.subheader("📊 Status")
        if st.session_state.transcript:
            st.success("✓ Transcript ready")
        if st.session_state.summary:
            st.success("✓ Summary ready")
        if st.session_state.quiz:
            st.success("✓ Quiz ready")

    # Process button
    if uploaded_file:
        if st.button("🚀 Process Video", type="primary", use_container_width=True):
            # Reset state
            st.session_state.transcript = None
            st.session_state.summary = None
            st.session_state.quiz = None
            st.session_state.user_answers = {}
            st.session_state.quiz_submitted = False

            # Process video
            result = process_video_complete(
                uploaded_file,
                num_questions,
                difficulty,
                summary_length
            )

            if result:
                st.session_state.transcript = result.get('transcript')
                st.session_state.summary = result.get('summary')
                st.session_state.quiz = result.get('quiz')
                st.success("✅ Video processed successfully!")
                st.balloons()

    # Display results
    if st.session_state.transcript or st.session_state.summary or st.session_state.quiz:
        st.write("---")

        # Tabs for different outputs
        tab1, tab2, tab3 = st.tabs(["📄 Transcript", "📝 Summary", "🎯 Quiz"])

        with tab1:
            if st.session_state.transcript:
                st.markdown('<p class="sub-header">Video Transcript</p>', unsafe_allow_html=True)

                with st.expander("View Full Transcript", expanded=False):
                    st.text_area(
                        "Transcript",
                        st.session_state.transcript,
                        height=400,
                        label_visibility="collapsed"
                    )

                # Download button
                st.download_button(
                    label="⬇️ Download Transcript",
                    data=st.session_state.transcript,
                    file_name="transcript.txt",
                    mime="text/plain"
                )

        with tab2:
            if st.session_state.summary:
                st.markdown('<p class="sub-header">Summary</p>', unsafe_allow_html=True)
                st.write(st.session_state.summary)

                st.write("\n")
                st.markdown("**Key Concepts:**")
                if 'key_concepts' in st.session_state and st.session_state.get('key_concepts'):
                    st.write(st.session_state.key_concepts)

                # Download button
                summary_text = f"SUMMARY\n{'='*50}\n\n{st.session_state.summary}"
                st.download_button(
                    label="⬇️ Download Summary",
                    data=summary_text,
                    file_name="summary.txt",
                    mime="text/plain"
                )

        with tab3:
            if st.session_state.quiz:
                display_quiz(st.session_state.quiz)

                col1, col2, col3 = st.columns([1, 1, 1])

                with col1:
                    if not st.session_state.quiz_submitted:
                        if st.button("✅ Submit Quiz", type="primary"):
                            st.session_state.quiz_submitted = True
                            st.rerun()

                with col2:
                    if st.session_state.quiz_submitted:
                        if st.button("🔄 Reset Quiz"):
                            st.session_state.user_answers = {}
                            st.session_state.quiz_submitted = False
                            st.rerun()

                # Display score
                if st.session_state.quiz_submitted:
                    correct, total = calculate_score(st.session_state.quiz)
                    percentage = (correct / total * 100) if total > 0 else 0

                    st.write("---")
                    st.markdown("### 🎯 Quiz Results")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Score", f"{correct}/{total}")
                    with col2:
                        st.metric("Percentage", f"{percentage:.1f}%")
                    with col3:
                        if percentage >= 70:
                            st.success("Great job! 🎉")
                        elif percentage >= 50:
                            st.info("Good effort! 👍")
                        else:
                            st.warning("Keep practicing! 📚")

                # Download quiz
                st.write("---")
                quiz_json = json.dumps(st.session_state.quiz, indent=2)
                st.download_button(
                    label="⬇️ Download Quiz (JSON)",
                    data=quiz_json,
                    file_name="quiz.json",
                    mime="application/json"
                )

    # Footer
    st.write("---")
    st.markdown("**Powered by OpenAI Whisper & GPT-4** | Built with Streamlit & Flask")

if __name__ == "__main__":
    main()
