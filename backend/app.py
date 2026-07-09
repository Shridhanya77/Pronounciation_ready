import os
import tempfile
from typing import Any, Dict

from flask import Flask, jsonify, request
from flask_cors import CORS

from config import DEBUG
from services.audio_validation import validate_audio_upload
from services.pronunciation_service import assess_file
from utils import get_logger, make_error_response

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
logger = get_logger(__name__)


@app.get("/health")
def health() -> Dict[str, Any]:
    return jsonify({"status": "ok", "service": "livo-ai-pronunciation"})


@app.post("/api/assess")
def assess() -> tuple[Dict[str, Any], int]:
    if "audio" not in request.files:
        payload, status_code = make_error_response("No audio file was uploaded.")
        return jsonify(payload), status_code

    uploaded_file = request.files["audio"]
    if uploaded_file.filename == "":
        payload, status_code = make_error_response("No audio file was uploaded.")
        return jsonify(payload), status_code

    try:
        validated = validate_audio_upload(uploaded_file)
        try:
            result = assess_file(validated["file_path"], validated)
            return jsonify(result)
        finally:
            if os.path.exists(validated["file_path"]):
                os.unlink(validated["file_path"])
    except ValueError as exc:
        logger.warning("Validation failed: %s", exc)
        payload, status_code = make_error_response(str(exc))
        return jsonify(payload), status_code
    except Exception as exc:  # pragma: no cover
        logger.exception("Assessment failed unexpectedly")
        payload, status_code = make_error_response("The assessment service is temporarily unavailable.")
        return jsonify(payload), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=DEBUG)
