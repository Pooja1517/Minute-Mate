import os
from flask import Flask, request, jsonify
import whisper
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize Whisper model
model = None

print("Starting Whisper API for Render...")

# Load Whisper model with Render-optimized settings
try:
    print("Loading Whisper model...")
    # Use tiny model for Render free tier to avoid memory issues
    model = whisper.load_model("tiny")
    print("Whisper tiny model loaded successfully!")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    model = None

# Notion Integration Setup
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "your-notion-integration-token-here")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "your-notion-database-id-here")

# Initialize Notion client (only if token is provided)
notion_client = None
try:
    from notion_client import Client
    if NOTION_TOKEN != "your-notion-integration-token-here":
        notion_client = Client(auth=NOTION_TOKEN)
        print("Notion client initialized successfully!")
except ImportError:
    print("Notion client not installed. Run: pip install notion-client")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "whisper_model_loaded": model is not None,
        "model_type": "tiny" if model else "none",
        "notion_available": notion_client is not None
    })

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if model is None:
        return jsonify({"error": "Whisper model not loaded. Please check the server logs."}), 500
    
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files["audio"]
    
    # Check file size - Very conservative for Render free tier
    file_size_mb = len(audio_file.read()) / (1024 * 1024)
    audio_file.seek(0)  # Reset file pointer
    
    if file_size_mb > 3:  # Very conservative limit for Render free tier
        return jsonify({"error": f"File too large ({file_size_mb:.1f} MB). Maximum size is 3 MB for Render free tier."}), 400
    
    print(f"Processing file: {file_size_mb:.1f} MB")
    
    # Use original file extension to preserve format
    original_filename = audio_file.filename
    file_extension = os.path.splitext(original_filename)[1] if original_filename else '.wav'
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
    
    try:
        # Save the uploaded file
        audio_file.save(tmp.name)
        tmp.close()
        
        print("Starting transcription with Render-optimized settings...")
        
        # Use very conservative settings for Render free tier
        result = model.transcribe(
            tmp.name, 
            fp16=False,  # Disable fp16 for better compatibility
            verbose=True,
            condition_on_previous_text=False,  # Disable for memory efficiency
            compression_ratio_threshold=2.4,   # More lenient threshold
            logprob_threshold=-1.0,            # More lenient threshold
            no_speech_threshold=0.6,           # More lenient threshold
            language=None,                     # Auto-detect language
            task="transcribe"                  # Explicitly set task
        )
        
        # Clean up
        os.unlink(tmp.name)
        
        if not result or not result.get("text"):
            return jsonify({"error": "Transcription returned empty result"}), 500
            
        print(f"Transcription successful: {len(result['text'])} characters")
        return jsonify({"text": result["text"]})
        
    except Exception as e:
        print(f"Transcription error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        
        # Clean up on error
        if os.path.exists(tmp.name):
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
        return jsonify({"error": str(e)}), 500

@app.route("/export/notion", methods=["POST"])
def export_to_notion():
    print("Notion export endpoint called")
    
    if notion_client is None:
        print("Notion client is None - integration not configured")
        return jsonify({"error": "Notion integration not configured. Please add your token and database ID."}), 500
    
    data = request.json
    print("Received data for Notion export:", data)
    
    transcript = data.get('transcript', '')
    title = data.get('title', 'Untitled Meeting')
    
    print(f"Transcript length: {len(transcript)}")
    print(f"Title: {title}")
    
    if not transcript:
        print("No transcript provided")
        return jsonify({"error": "No transcript provided"}), 400
    
    try:
        print("Creating Notion page...")
        
        # Create blocks for the Notion page
        children = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📝 Meeting Transcript"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": transcript}}]
                }
            }
        ]
        
        print(f"Creating page with {len(children)} blocks")
        print(f"Database ID: {NOTION_DATABASE_ID}")
        
        # Create the page in Notion
        response = notion_client.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": f"Meeting Notes - {title}"
                            }
                        }
                    ]
                }
            },
            children=children
        )
        
        print("Notion page created successfully:", response["id"])
        return jsonify({
            "success": True,
            "message": "Successfully exported to Notion!",
            "page_id": response["id"]
        })
        
    except Exception as e:
        print(f"Error exporting to Notion: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Failed to export to Notion: {str(e)}"}), 500

@app.route("/export/google-docs", methods=["POST"])
def export_to_google_docs():
    print("Google Docs export endpoint called")
    
    data = request.json
    print("Received data for Google Docs export:", data)
    
    transcript = data.get('transcript', '')
    title = data.get('title', 'Untitled Meeting')
    
    print(f"Transcript length: {len(transcript)}")
    print(f"Title: {title}")
    
    if not transcript:
        print("No transcript provided")
        return jsonify({"error": "No transcript provided"}), 400
    
    try:
        # For Google Docs, we'll return a formatted text that can be copied
        # In a full implementation, you'd use Google Docs API
        formatted_text = f"""
# {title}

## Meeting Transcript

{transcript}

---
*Generated by Minute Mate on {os.getenv('RENDER_SERVICE_NAME', 'Render')}*
        """.strip()
        
        print("Google Docs export prepared successfully")
        return jsonify({
            "success": True,
            "message": "Text formatted for Google Docs. Copy and paste into a new Google Doc.",
            "formatted_text": formatted_text,
            "instructions": "Copy the formatted text above and paste it into a new Google Doc"
        })
        
    except Exception as e:
        print(f"Error preparing Google Docs export: {e}")
        return jsonify({"error": f"Failed to prepare Google Docs export: {str(e)}"}), 500

@app.route("/test-notion", methods=["GET"])
def test_notion():
    print("Testing Notion integration...")
    
    if notion_client is None:
        return jsonify({"error": "Notion client not initialized"}), 500
    
    try:
        # Try to read the database to test access
        response = notion_client.databases.retrieve(database_id=NOTION_DATABASE_ID)
        return jsonify({
            "success": True,
            "message": "Notion integration is working!",
            "database_title": response.get("title", [{}])[0].get("text", {}).get("content", "Unknown")
        })
    except Exception as e:
        print(f"Notion test error: {e}")
        return jsonify({"error": f"Notion test failed: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "Whisper API for Render with Export Features",
        "status": "running",
        "model_loaded": model is not None,
        "notion_available": notion_client is not None,
        "features": [
            "audio_transcription",
            "notion_export", 
            "google_docs_export"
        ]
    })

if __name__ == "__main__":
    # Use environment variables for production deployment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_ENV") == "development"
    
    print(f"Starting Whisper API on {host}:{port}")
    app.run(host=host, port=port, debug=debug) 