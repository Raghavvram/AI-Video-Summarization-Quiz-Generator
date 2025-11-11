import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""

    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # File paths
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'outputs'

    # File limits
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

    # API settings
    API_HOST = '0.0.0.0'
    API_PORT = 5000
    DEBUG = True

    # Model settings
    WHISPER_MODEL = 'whisper-1'
    GPT_MODEL = 'gpt-4'

    # Default values
    DEFAULT_NUM_QUESTIONS = 5
    DEFAULT_DIFFICULTY = 'medium'
    DEFAULT_SUMMARY_LENGTH = 'medium'

    @staticmethod
    def validate():
        """Validate configuration."""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)

        print("Configuration validated successfully!")
        return True

if __name__ == "__main__":
    Config.validate()
    print(f"Upload folder: {Config.UPLOAD_FOLDER}")
    print(f"Output folder: {Config.OUTPUT_FOLDER}")
