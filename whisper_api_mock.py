import os
import tempfile
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files["audio"]
    
    # Mock transcription - returns a sample transcript
    sample_transcripts = [
        "Hello everyone, thank you for joining today's meeting. Let's discuss our project progress and next steps.",
        "Good morning team, I hope everyone is doing well. Today we'll review our quarterly goals and achievements.",
        "Welcome to our weekly standup meeting. Let's go around the room and share our updates and any blockers."
    ]
    
    mock_transcript = random.choice(sample_transcripts)
    
    return jsonify({"text": mock_transcript})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    transcript = data.get('transcript', '')
    
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400
    
    try:
        # Simple rule-based summarization
        sentences = transcript.split('.')
        summary = '. '.join(sentences[:2]) + '.'  # Take first 2 sentences
        
        # Simple action item extraction
        action_items = []
        action_keywords = ['will', 'going to', 'need to', 'should', 'must', 'have to', 'let\'s', 'we should']
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in action_keywords):
                action_items.append(sentence.strip())
        
        if not action_items:
            action_items = ["Review project progress", "Schedule follow-up meeting", "Update team documentation"]
        
        return jsonify({
            'summary': summary,
            'action_items': action_items[:3]  # Limit to 3 items
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "whisper-api-mock"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False) 