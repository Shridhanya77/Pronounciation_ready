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


def _get_audio_magic_bytes(stream) -> bytes:
    """Read first few bytes to validate audio signature."""
    stream.seek(0)
    header = stream.read(512)
    stream.seek(0)
    return header


def _is_supported_header(header: bytes, extension: str) -> bool:
    """Basic file signature validation."""

    if extension == "wav":
        return header.startswith(b"RIFF")

    elif extension == "mp3":
        return (
            header.startswith(b"ID3")
            or header[:2] == b"\xff\xfb"
            or header[:2] == b"\xff\xfa"
        )

    elif extension == "m4a":
        return b"ftyp" in header

    return False


def _get_duration_seconds(file_path: str, extension: str) -> float:
    """Calculate duration of uploaded audio."""

    if extension == "wav":
        with wave.open(file_path, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            if rate == 0:
                return 0.0
            return frames / float(rate)

    elif extension == "mp3":
        if MP3 is None:
            raise RuntimeError("mutagen is required for MP3 support")
        return float(MP3(file_path).info.length)

    elif extension == "m4a":
        if MP4 is None:
            raise RuntimeError("mutagen is required for M4A support")
        return float(MP4(file_path).info.length)

    return 0.0


def validate_audio_upload(file_storage) -> Dict[str, Any]:
    """
    Validate uploaded audio file.

    Returns
    -------
    dict
        {
            file_path,
            filename,
            extension,
            duration_seconds,
            size_bytes
        }
    """

    if file_storage is None:
        raise ValueError("No audio file uploaded.")

    filename = secure_filename(file_storage.filename or "")

    if not filename:
        raise ValueError("No filename provided.")

    if "." not in filename:
        raise ValueError("File has no extension.")

    extension = filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    header = _get_audio_magic_bytes(file_storage.stream)

    if not _is_supported_header(header, extension):
        raise ValueError("Invalid or corrupted audio file.")

    mime_type = (file_storage.mimetype or "").lower()

    if mime_type and mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError("Unsupported MIME type.")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{extension}"
    ) as temp_file:

        file_storage.stream.seek(0)
        file_storage.save(temp_file.name)
        file_path = temp_file.name

    size_bytes = os.path.getsize(file_path)

    if size_bytes > MAX_FILE_SIZE_BYTES:
        os.remove(file_path)
        raise ValueError("Maximum file size is 20 MB.")

    duration = _get_duration_seconds(file_path, extension)

    if duration < MIN_DURATION_SECONDS:
        os.remove(file_path)
        raise ValueError("Audio must be at least 30 seconds.")

    if duration > MAX_DURATION_SECONDS:
        os.remove(file_path)
        raise ValueError("Audio cannot exceed 45 seconds.")

    logger.info(
        "Validated audio %s (%.2fs)",
        filename,
        duration,
    )

    return {
        "file_path": file_path,
        "filename": filename,
        "extension": extension,
        "duration_seconds": round(duration, 2),
        "size_bytes": size_bytes,
    }