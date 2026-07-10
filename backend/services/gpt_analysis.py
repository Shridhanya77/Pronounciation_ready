import json
import os
from typing import Any, Dict, List

from ..utils import get_logger, sanitize_text

logger = get_logger(__name__)


def _build_local_feedback(
    transcript: str,
    word_confidences: List[Dict[str, Any]],
    speech_metadata: Dict[str, Any],
) -> Dict[str, Any]:

    words = [entry["word"] for entry in word_confidences if entry.get("word")]

    mistakes = []

    for entry in word_confidences[:5]:
        if entry.get("confidence", 1.0) < 0.8:
            mistakes.append(
                {
                    "word": entry["word"],
                    "type": "Pronunciation hint",
                    "reason": "The word was less clear than expected in the audio sample.",
                    "suggestion": "Repeat the word slowly and place extra emphasis on the stressed syllable.",
                }
            )

    if not mistakes and words:
        mistakes.append(
            {
                "word": words[0],
                "type": "Pronunciation hint",
                "reason": "A short practice pass could help improve overall clarity.",
                "suggestion": "Read the sentence slowly and focus on each word individually.",
            }
        )

    return {
        "overall_explanation": (
            "Your delivery sounds clear overall. "
            "A few words could be spoken more deliberately "
            "to improve articulation and confidence."
        ),
        "mistakes": mistakes,
        "general_suggestions": [
            "Keep a steady pace and avoid rushing.",
            "Practice the most difficult words in isolation.",
            "Record another take and compare your clarity.",
        ],
        "metadata": speech_metadata,
    }


def generate_explanations(
    transcript: str,
    word_confidences: List[Dict[str, Any]],
    speech_metadata: Dict[str, Any],
) -> Dict[str, Any]:

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key and transcript:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)

            prompt = (
                "You are an English pronunciation coach. "
                "Use the transcript, word confidence estimates, "
                "and speech metadata only to explain pronunciation quality. "
                "Generate a learner-friendly explanation, list of mistakes, "
                "and improvement tips. "
                "Return ONLY valid JSON with keys "
                "overall_explanation, mistakes, general_suggestions."
                f"\nTranscript: {transcript}"
                f"\nWord confidence: {json.dumps(word_confidences)}"
                f"\nMetadata: {json.dumps(speech_metadata)}"
            )

            response = client.responses.create(
                model="gpt-4o-mini",
                input=prompt,
                temperature=0.2,
            )

            content = getattr(response, "output_text", "")

            if content:
                parsed = json.loads(content)

                return {
                    "overall_explanation": sanitize_text(
                        parsed.get("overall_explanation", "")
                    ),
                    "mistakes": parsed.get("mistakes", []),
                    "general_suggestions": parsed.get(
                        "general_suggestions", []
                    ),
                    "metadata": speech_metadata,
                }

        except Exception as exc:
            logger.warning("GPT explanation generation failed: %s", exc)

    return _build_local_feedback(
        transcript,
        word_confidences,
        speech_metadata,
    )