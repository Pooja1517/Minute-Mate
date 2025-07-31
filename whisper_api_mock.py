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
    
    # Mock transcription - returns a comprehensive sample transcript
    sample_transcripts = [
        """Hello everyone, thank you for joining today's meeting. Let's discuss our project progress and next steps. We've made significant progress on the frontend development, with the React components now fully functional. The backend API integration is also complete, and we've successfully implemented the Google Docs export feature. However, we still need to address some performance issues and complete the testing phase. Our next milestone is to deploy the application to production and conduct user acceptance testing. We should also schedule a review meeting with the stakeholders to get their feedback on the current implementation. Let's make sure we have all the necessary documentation ready for the deployment process.""",
        
        """Good morning team, I hope everyone is doing well. Today we'll review our quarterly goals and achievements. We've successfully completed 85% of our planned objectives for this quarter. The mobile app development is on track, with the iOS version ready for beta testing. The Android version is expected to be completed by next week. Our marketing campaign has generated 150% more leads than expected, which is excellent news. However, we need to focus on improving our customer support response time, as it's currently taking longer than our target of 2 hours. We should also prioritize the implementation of the new payment gateway integration. Let's discuss the resource allocation for the upcoming projects and ensure we have enough developers assigned to each team.""",
        
        """Welcome to our weekly standup meeting. Let's go around the room and share our updates and any blockers. Sarah has completed the user authentication module and is now working on the password reset functionality. Mike finished the database optimization and reports a 40% improvement in query performance. Lisa is still working on the third-party API integration and has encountered some authentication issues that need to be resolved. John completed the frontend responsive design updates and is ready to move on to the next sprint. We have a few blockers that need attention: the server deployment is taking longer than expected due to configuration issues, and we're waiting for approval on the new design mockups. Let's prioritize these issues and assign resources accordingly. Also, don't forget about the upcoming client presentation on Friday."""
    ]
    
    # Choose transcript based on file size for variety
    file_size = len(audio_file.read())
    audio_file.seek(0)  # Reset file pointer
    
    if file_size < 100000:  # Small file
        mock_transcript = sample_transcripts[0]
    elif file_size < 500000:  # Medium file
        mock_transcript = sample_transcripts[1]
    else:  # Large file
        mock_transcript = sample_transcripts[2]
    
    return jsonify({"text": mock_transcript})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    transcript = data.get('transcript', '')
    
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400
    
    try:
        # Enhanced rule-based summarization for longer transcripts
        sentences = [s.strip() for s in transcript.split('.') if s.strip()]
        
        # Create a comprehensive summary (first 3-4 sentences)
        if len(sentences) <= 3:
            summary = transcript
        else:
            # Take first 4 sentences but ensure we get a good summary
            summary_sentences = sentences[:4]
            summary = '. '.join(summary_sentences) + '.'
            
            # If summary is too short, add more sentences
            if len(summary) < 200 and len(sentences) > 4:
                summary = '. '.join(sentences[:6]) + '.'
        
        # Enhanced action item extraction
        action_items = []
        action_keywords = [
            'will', 'going to', 'need to', 'should', 'must', 'have to', 
            'let\'s', 'we should', 'need to', 'have to', 'must', 'should',
            'schedule', 'plan', 'review', 'implement', 'deploy', 'test',
            'complete', 'finish', 'start', 'begin', 'prepare', 'organize'
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in action_keywords):
                # Clean up the action item
                clean_action = sentence.strip()
                if clean_action and len(clean_action) > 10:  # Avoid very short items
                    action_items.append(clean_action)
        
        # If no action items found, generate some based on content
        if not action_items:
            if 'meeting' in transcript.lower():
                action_items = ["Schedule follow-up meeting", "Send meeting minutes to team", "Review action items from meeting"]
            elif 'project' in transcript.lower():
                action_items = ["Review project progress", "Update project documentation", "Schedule project review"]
            else:
                action_items = ["Review progress", "Schedule follow-up", "Update documentation"]
        
        return jsonify({
            'summary': summary,
            'action_items': action_items[:5]  # Allow up to 5 items
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "whisper-api-mock"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False) 