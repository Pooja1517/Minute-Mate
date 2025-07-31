import os
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files["audio"]
    filename = audio_file.filename
    
    print(f"Processing audio file: {filename}")
    
    # Enhanced mock transcription with realistic content
    base_transcripts = [
        "Hello everyone, thank you for joining today's meeting. Let's discuss our project progress and next steps. I'd like to start by reviewing our current status and then move on to action items.",
        "Good morning team, I hope everyone is doing well. Today we'll review our quarterly goals and achievements. We've made significant progress on several key initiatives.",
        "Welcome to our weekly standup meeting. Let's go around the room and share our updates and any blockers. I'll start with my updates, then we'll hear from each team member.",
        "Thank you all for attending this important meeting. We have several critical items to discuss today, including project timelines, resource allocation, and upcoming deadlines.",
        "Hi everyone, welcome to our project review meeting. We'll be covering the current sprint progress, upcoming milestones, and any issues that need immediate attention."
    ]
    
    # Get file size to determine transcript length
    file_size = len(audio_file.read())
    audio_file.seek(0)  # Reset file pointer
    
    # Generate transcript based on file size
    if file_size > 1000000:  # Large file (>1MB)
        extended_content = " We also need to address the technical challenges we've encountered and discuss potential solutions. The team has been working hard on this project, and I'm confident we can meet our deadlines."
        mock_transcript = random.choice(base_transcripts) + extended_content
    else:  # Small file
        mock_transcript = random.choice(base_transcripts)
    
    print(f"Mock transcription completed: {len(mock_transcript)} characters")
    return jsonify({"text": mock_transcript, "method": "minimal_mock"})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    transcript = data.get('transcript', '')
    
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400
    
    try:
        # Simple summarization
        sentences = [s.strip() for s in transcript.split('.') if s.strip()]
        summary = '. '.join(sentences[:2]) + '.' if len(sentences) > 1 else transcript
        
        # Simple action item extraction
        action_items = []
        action_keywords = ['will', 'going to', 'need to', 'should', 'must', 'have to', 'let\'s']
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in action_keywords):
                action = sentence.strip()
                if action.endswith('.'):
                    action = action[:-1]
                action_items.append(action)
        
        if not action_items:
            action_items = ["Review the meeting transcript", "Schedule follow-up meeting", "Update documentation"]
        
        return jsonify({
            'summary': summary,
            'action_items': action_items[:3]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy", 
        "service": "whisper-api-minimal",
        "method": "minimal_mock",
        "deployment": "guaranteed"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False) 