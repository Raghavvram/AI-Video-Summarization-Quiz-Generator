import os
from openai import OpenAI
from moviepy.editor import VideoFileClip
import time

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_audio(video_path, audio_path="temp_audio.mp3"):
    """Extract audio from video file."""
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path, verbose=False, logger=None)
        video.close()
        return audio_path
    except Exception as e:
        raise Exception(f"Error extracting audio: {str(e)}")

def transcribe_audio(audio_path, language=None):
    """Transcribe audio using OpenAI Whisper API."""
    try:
        with open(audio_path, "rb") as audio_file:
            # Check file size (Whisper has 25MB limit)
            file_size = os.path.getsize(audio_path)
            if file_size > 25 * 1024 * 1024:  # 25MB
                raise Exception("Audio file too large. Please use video < 25MB or implement chunking.")

            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )
        return transcript
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")

def process_video_transcription(video_path):
    """Complete pipeline: video -> audio -> transcript."""
    print(f"Processing video: {video_path}")

    # Extract audio
    audio_path = extract_audio(video_path)
    print(f"Audio extracted to: {audio_path}")

    # Transcribe
    transcript = transcribe_audio(audio_path)
    print("Transcription completed!")

    # Clean up temporary audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return transcript.text, transcript.segments if hasattr(transcript, 'segments') else []

if __name__ == "__main__":
    # Test the transcription module
    video_file = "test_video.mp4"
    if os.path.exists(video_file):
        text, segments = process_video_transcription(video_file)
        print(f"\nTranscript:\n{text[:500]}...")
    else:
        print("No test video found. Place a video file named 'test_video.mp4' to test.")
