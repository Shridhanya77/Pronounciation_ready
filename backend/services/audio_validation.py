import os
import tempfile
import wave
from typing import Dict, Any

from werkzeug.utils import secure_filename

from config import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, MAX_DURATION_SECONDS, MAX_FILE_SIZE_BYTES, MIN_DURATION_SECONDS
from utils import get_logger

try:
    from mutagen.mp3 import MP3
except Exception:  # pragma: no cover
    MP3 = None

try:
    from mutagen.mp4 import MP4
except Exception:  # pragma: no cover
    MP4 = None

logger = get_logger(__name__)


def _get_audio_magic_bytes(stream) -> bytes:
    stream.seek(0)
    return stream.read(512)


def _is_supported_header(header: bytes, extension: str) -> bool:
    if extension == "wav":
        return header.startswith(b"RIFF")
    if extension == "mp3":
        return header.startswith(b"ID3") or header[0:2] in {b"\xff\xfb", b"\xff\xfa"}
    if extension == "m4a":
        return b"ftyp" in header or b"moov" in header or b"mdat" in header
    return False


def _get_duration_seconds(file_path: str, extension: str) -> float:
    if extension == "wav":
        with wave.open(file_path, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            return float(frames) / float(rate) if rate else 0.0
    if extension == "mp3" and MP3 is not None:
        return float(MP3(file_path).info.length)
    if extension == "m4a" and MP4 is not None:
        return float(MP4(file_path).info.length)
    return 0.0


def validate_audio_upload(file_storage) -> Dict[str, Any]:
    filename = secure_filename(file_storage.filename or "")
    if not filename:
        raise ValueError("No file selected. Please choose an audio recording.")

    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Please upload a WAV, MP3, or M4A recording.")

    header = _get_audio_magic_bytes(file_storage.stream)
    if not _is_supported_header(header, extension):
        raise ValueError("The uploaded file does not look like a valid audio file.")

    mime_type = (file_storage.mimetype or "").lower()
    if mime_type and mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError("The uploaded file has an unsupported MIME type.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension}") as temp_file:
        file_storage.stream.seek(0)
        file_storage.save(temp_file.name)
        file_path = temp_file.name

    size_bytes = os.path.getsize(file_path)
    if size_bytes > MAX_FILE_SIZE_BYTES:
        os.unlink(file_path)
        raise ValueError("The selected file is too large. Maximum size is 20 MB.")

    duration_seconds = _get_duration_seconds(file_path, extension)
    if duration_seconds < MIN_DURATION_SECONDS:
        os.unlink(file_path)
        raise ValueError("The recording is too short. Please upload a file between 30 and 45 seconds long.")
    if duration_seconds > MAX_DURATION_SECONDS:
        os.unlink(file_path)
        raise ValueError("The recording is too long. Please upload a file between 30 and 45 seconds long.")

    logger.info("Validated audio upload: %s (%s bytes, %.2f seconds)", filename, size_bytes, duration_seconds)
    return {
        "file_path": file_path,
        "filename": filename,
        "size_bytes": size_bytes,
        "duration_seconds": round(duration_seconds, 2),
        "extension": extension,
    }
