import os
import tempfile
import wave
from typing import Dict, Any

from werkzeug.utils import secure_filename

from ..config import (
    ALLOWED_EXTENSIONS,
    ALLOWED_MIME_TYPES,
    MAX_DURATION_SECONDS,
    MAX_FILE_SIZE_BYTES,
    MIN_DURATION_SECONDS,
)

from ..utils import get_logger

try:
    from mutagen.mp3 import MP3
except Exception:
    MP3 = None

try:
    from mutagen.mp4 import MP4
except Exception:
    MP4 = None

logger = get_logger(__name__)