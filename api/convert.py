from flask import Blueprint, request, send_file
import tempfile
import subprocess
import os

convert_to_mp4 = Blueprint('convert_to_mp4', __name__)

@convert_to_mp4.route("/api/convert-to-mp4", methods=["POST"])
def convert_to_mp4():
    if "video" not in request.files:
        return "No video file", 400

    video = request.files["video"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_input:
        video.save(temp_input)
        temp_input_path = temp_input.name

    temp_output_path = temp_input_path.replace(".webm", ".mp4")

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                temp_input_path,
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                temp_output_path,
            ],
            check=True,
        )

        return send_file(
            temp_output_path, as_attachment=True, download_name="converted_video.mp4"
        )
    except subprocess.CalledProcessError as e:
        return f"Conversion failed: {str(e)}", 500
    finally:
        os.unlink(temp_input_path)
        if os.path.exists(temp_output_path):
            os.unlink(temp_output_path)
