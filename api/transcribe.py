from flask import Blueprint, request, jsonify
import requests
import os
import io
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

transcribe = Blueprint('transcribe', __name__)

@transcribe.route("/api/transcribe", methods=["POST"])
def transcribe_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400

    video_file = request.files["video"]
    video = io.BytesIO(video_file.read())

    try:
        url = "https://api.symphoniclabs.com/transcribe"
        api_key = os.getenv("SYMPHONIC_API_KEY")  # Get the API key from the environment variable

        response = requests.post(
            url,
            files={"video": ("input.webm", video, "video/webm")},
            headers={"Authorization": f"Bearer {api_key}"}  # Use the API key in the header if required
        )
        response.raise_for_status()
        transcribed_text = response.json().get("transcription", "")
        return jsonify({"transcription": transcribed_text})
    except requests.exceptions.RequestException as e:
        print(f"Error calling Symphonic Labs API: {e}")
        return jsonify({"error": "Failed to transcribe video"}), 500
