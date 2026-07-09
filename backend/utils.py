import logging
import os
from typing import Any, Dict


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def make_error_response(message: str, status_code: int = 400, extra: Dict[str, Any] | None = None) -> tuple[Dict[str, Any], int]:
    payload = {"error": message}
    if extra:
        payload.update(extra)
    return payload, status_code


def sanitize_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())
