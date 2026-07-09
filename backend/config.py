import os
from dotenv import load_dotenv

load_dotenv()

MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_FILE_SIZE_BYTES", str(20 * 1024 * 1024)))
MIN_DURATION_SECONDS = int(os.getenv("MIN_DURATION_SECONDS", "30"))
MAX_DURATION_SECONDS = int(os.getenv("MAX_DURATION_SECONDS", "45"))
ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a"}
ALLOWED_MIME_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp3",
    "audio/mp4",
    "audio/x-m4a",
    "audio/m4a",
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
AZURE_SPEECH_ENDPOINT = os.getenv("AZURE_SPEECH_ENDPOINT")

DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in {"1", "true", "yes"}
