import os
import tempfile
from flask import Flask, request, jsonify
import whisper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Whisper model
model = whisper.load_model("base")  # Using smaller model for Render

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files["audio"]
    tmp = tempfile.NamedTemporaryFile(delete=False)
    
    try:
        audio_file.save(tmp.name)
        tmp.close()
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

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    transcript = data.get('transcript', '')
    
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400
    
    try:
        # Simple rule-based summarization for Render
        sentences = transcript.split('.')
        summary = '. '.join(sentences[:3]) + '.'  # Take first 3 sentences
        
        # Simple action item extraction
        action_items = []
        words = transcript.lower().split()
        action_keywords = ['will', 'going to', 'need to', 'should', 'must', 'have to']
        
        sentences = transcript.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in action_keywords):
                action_items.append(sentence.strip())
        
        if not action_items:
            action_items = ["No specific action items identified"]
        
        return jsonify({
            'summary': summary,
            'action_items': action_items[:5]  # Limit to 5 items
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "whisper-api"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False) 