from flask import Flask
from api.transcribe import transcribe
from api.convert_to_mp4 import convert_to_mp4

app = Flask(__name__)

# Register blueprints
app.register_blueprint(transcribe)
app.register_blueprint(convert_to_mp4)

if __name__ == "__main__":
    app.run(debug=True)
