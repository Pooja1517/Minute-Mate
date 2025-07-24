import os
os.environ["PATH"] += os.pathsep + r"C:\Users\T1IN\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

from flask import Flask, request, jsonify
import whisper
import tempfile

app = Flask(__name__)
model = whisper.load_model("small")  # or "base", "medium", "large"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    audio_file = request.files["audio"]
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        audio_file.save(tmp.name)
        tmp.close()  # Ensure file is closed before Whisper reads it
        result = model.transcribe(tmp.name)
        os.unlink(tmp.name)
        return jsonify({"text": result["text"]})
    except Exception as e:
        if os.path.exists(tmp.name):
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) 