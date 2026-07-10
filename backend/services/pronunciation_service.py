import os
import tempfile
from typing import Any, Dict

from .gpt_analysis import generate_explanations
from .speech_service import assess_audio as run_speech_assessment
from ..utils import get_logger

logger = get_logger(__name__)


def assess_file(file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess pronunciation for an uploaded audio file.
    """

    speech_result = run_speech_assessment(file_path, metadata)

    transcript = speech_result.get("transcript", "")
    word_confidences = speech_result.get("word_confidences", [])

    explanation = generate_explanations(
        transcript=transcript,
        word_confidences=word_confidences,
        speech_metadata={
            "duration_seconds": metadata.get("duration_seconds"),
            "filename": metadata.get("filename"),
            "engine": speech_result.get("engine", "unknown"),
        },
    )

    mistakes = speech_result.get(
        "mistakes",
        explanation.get("mistakes", [])
    )

    general_suggestions = speech_result.get(
        "general_suggestions",
        explanation.get("general_suggestions", [])
    )

    return {
        "overall_score": speech_result.get("overall_score", 80),
        "accuracy": speech_result.get("accuracy", 80),
        "fluency": speech_result.get("fluency", 80),
        "completeness": speech_result.get("completeness", 80),
        "transcript": transcript,
        "mistakes": mistakes,
        "general_suggestions": general_suggestions,
        "engine": speech_result.get("engine", "fallback-simulation"),
        "explanation": explanation.get("overall_explanation", ""),
    }