import os
from typing import Any, Dict

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.config import DEBUG
from backend.services.audio_validation import validate_audio_upload
from backend.services.pronunciation_service import assess_file
from backend.utils import get_logger, make_error_response

app = Flask(__name__)
CORS(app)

logger = get_logger(__name__)


# -------------------------------
# Home Route
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "Livo AI Pronunciation Assessment API is running successfully."
    })


# -------------------------------
# Health Check
# -------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "livo-ai-pronunciation"
    })


# -------------------------------
# Assessment Endpoint
# -------------------------------
@app.route("/api/assess", methods=["POST"])
def assess():

    if "audio" not in request.files:
        payload, status = make_error_response("No audio file uploaded.")
        return jsonify(payload), status

    uploaded_file = request.files["audio"]

    if uploaded_file.filename == "":
        payload, status = make_error_response("No audio file selected.")
        return jsonify(payload), status

    try:
        validated = validate_audio_upload(uploaded_file)

        result = assess_file(
            validated["file_path"],
            validated
        )

        if os.path.exists(validated["file_path"]):
            os.remove(validated["file_path"])

        return jsonify(result), 200

    except ValueError as e:

        payload, status = make_error_response(str(e))
        return jsonify(payload), status

    except Exception as e:

        logger.exception(e)

        payload, status = make_error_response(
            "Internal Server Error"
        )

        return jsonify(payload), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=DEBUG
    )