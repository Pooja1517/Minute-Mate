import os
# Remove Windows-specific ffmpeg path for Render deployment
# os.environ["PATH"] += os.pathsep + r"C:\Users\T1IN\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

from flask import Flask, request, jsonify
import whisper
import tempfile
from transformers import pipeline
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize models as None first, then load them
model = None
summarizer = None
action_item_extractor = None

print("Starting Whisper API...")

# Load Whisper model - model size configurable via env, default to base for Render free tier
try:
    whisper_model_name = os.getenv("WHISPER_MODEL", "tiny") # Use tiny model for Render free tier to reduce memory usage
    print(f"Loading Whisper model: {whisper_model_name}...")
    model = whisper.load_model(whisper_model_name)
    print("Whisper model loaded successfully!")
except Exception as e:
    print(f"Error loading Whisper model '{os.getenv('WHISPER_MODEL', 'base')}': {e}")
    # Fallback to tiny model if configured model fails
    try:
        print("Trying tiny model as fallback...")
        model = whisper.load_model("tiny")
        print("Tiny Whisper model loaded successfully!")
    except Exception as e2:
        print(f"Error loading tiny model: {e2}")
        model = None

# Load summarization model (optional for memory-constrained environments)
    try:
        if os.getenv("ENABLE_SUMMARIZATION", "false").lower() == "true":
            print("Loading summarization model...")
            summarization_model = pipeline("summarization", model="facebook/bart-large-cnn")
            print("Summarization model loaded successfully!")
        else:
            print("Summarization disabled to save memory (set ENABLE_SUMMARIZATION=true to enable)")
            summarization_model = None
    except Exception as e:
        print(f"Warning: Could not load summarization model: {e}")
        print("Continuing without summarization capability...")
        summarization_model = None

# Use a small T5 model for extracting action items
# This model is not perfect, but will extract tasks in plain English
# For more advanced extraction, a custom fine-tuned model would be needed
try:
    action_item_extractor = pipeline("text2text-generation", model="mrm8488/t5-base-finetuned-question-generation-ap")
except Exception as e:
    action_item_extractor = None  # Fallback if model fails to load

# Notion Integration Setup
# Replace these with your actual values from Step 1 and Step 4
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "your-notion-integration-token-here")  # From Step 1
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "your-notion-database-id-here")  # From Step 4

# Initialize Notion client (only if token is provided)
notion_client = None
try:
    from notion_client import Client
    if NOTION_TOKEN != "your-notion-integration-token-here":
        notion_client = Client(auth=NOTION_TOKEN)
except ImportError:
    print("Notion client not installed. Run: pip install notion-client")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "whisper_model_loaded": model is not None,
        "summarizer_loaded": summarizer is not None,
        "action_extractor_loaded": action_item_extractor is not None
    })

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if model is None:
        return jsonify({"error": "Whisper model not loaded. Please check the server logs."}), 500
    
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files["audio"]
    
    # Check file size - Reduced limit for Render free tier
    file_size_mb = len(audio_file.read()) / (1024 * 1024)
    audio_file.seek(0)  # Reset file pointer
    
    if file_size_mb > 5:  # Reduced from 10MB to 5MB for Render free tier
        return jsonify({"error": f"File too large ({file_size_mb:.1f} MB). Maximum size is 5 MB for Render free tier."}), 400
    
    print(f"File size: {file_size_mb:.1f} MB")
    
    # Use original file extension to preserve format
    original_filename = audio_file.filename
    file_extension = os.path.splitext(original_filename)[1] if original_filename else '.wav'
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
    
    try:
        # Save the uploaded file
        audio_file.save(tmp.name)
        tmp.close()
        
        file_size_mb = os.path.getsize(tmp.name) / (1024 * 1024)
        print(f"Processing file: {original_filename} ({file_size_mb:.1f} MB)")
        
        # Optimized settings for Render free tier
        print("Starting transcription with optimized settings for Render...")
        
        # Use conservative settings for Render free tier
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

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    transcript = data.get('transcript', '')
    print("Received transcript for summarization:", len(transcript), "characters")
    
    if not transcript:
        print("No transcript provided.")
        return jsonify({"error": "No transcript provided"}), 400
    
    if summarization_model is None:
        return jsonify({"error": "Summarization model not loaded. Please check the server logs."}), 500
    
    try:
        # Add delay to prevent memory issues
        import time
        time.sleep(0.1)
        
        # Prompt the summarizer for bullet points and decisions
        prompt = "Summarize the following meeting transcript as bullet points, including key decisions if any:\n" + transcript
        summary = summarization_model(prompt, max_length=80, min_length=10, do_sample=False)[0]['summary_text']
        print("Summary generated:", len(summary), "characters")
        
        if not summary.strip():
            summary = "No summary could be generated for this transcript."
            
        action_items = extract_action_items(transcript)
        print("Action items extracted:", len(action_items), "items")
        
        return jsonify({'summary': summary, 'action_items': action_items})
        
    except Exception as e:
        print("Error in summarization:", e)
        return jsonify({"error": str(e)}), 500

# Extract action items using a prompt-based T5 model
# Returns a list of action items, including responsible persons and deadlines if present
# Falls back to rule-based extraction if T5 model is unavailable

def extract_action_items(text):
    # Try model-based extraction first
    if action_item_extractor is not None:
        prompt = f"Extract action items (tasks, owners, deadlines) as bullet points from this meeting transcript: {text}"
        try:
            result = action_item_extractor(prompt, max_length=128, do_sample=False)[0]['generated_text']
            items = [item.strip('- ').strip() for item in result.split('\n') if item.strip()]
            return items if items else ["No action items found."]
        except Exception:
            pass  # Fallback to rule-based

    # Improved rule-based fallback
    import re
    lines = re.split(r'[\n\.\!\?]', text)
    keywords = ['will', 'must', 'should', 'need to', 'assign', 'deadline', 'by', 'complete', 'finish', 'prepare', 'send', 'review', 'schedule', 'put up', 'remind', 'meet', 'help', 'share']
    actions = []
    for line in lines:
        l = line.strip()
        if not l:
            continue
        # Look for lines that start with a verb or contain a keyword
        if any(l.lower().startswith(word) or word in l.lower() for word in keywords):
            actions.append(l)
    return actions if actions else ["No action items found."]

@app.route("/export/notion", methods=["POST"])
def export_to_notion():
    print("Notion export endpoint called")
    
    if notion_client is None:
        print("Notion client is None - integration not configured")
        return jsonify({"error": "Notion integration not configured. Please add your token and database ID."}), 500
    
    data = request.json
    print("Received data:", data)
    
    transcript = data.get('transcript', '')
    summary = data.get('summary', '')
    action_items = data.get('actions', [])
    
    print(f"Transcript length: {len(transcript)}")
    print(f"Summary: {summary}")
    print(f"Action items: {action_items}")
    
    if not transcript and not summary:
        print("No transcript or summary provided")
        return jsonify({"error": "No transcript or summary provided"}), 400
    
    try:
        print("Creating Notion page...")
        # Create blocks for the Notion page
        children = []
        
        # Add summary section
        if summary:
            children.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📋 Meeting Summary"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": summary}}]
                    }
                }
            ])
        
        # Add action items section
        if action_items and len(action_items) > 0:
            children.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "✅ Action Items"}}]
                    }
                }
            ])
            
            for item in action_items:
                if item and item.strip():
                    children.append({
                        "object": "block",
                        "type": "to_do",
                        "to_do": {
                            "rich_text": [{"type": "text", "text": {"content": item.strip()}}],
                            "checked": False
                        }
                    })
        
        # Add full transcript (collapsed)
        if transcript:
            children.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📝 Full Transcript"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [{"type": "text", "text": {"content": "Click to expand"}}],
                        "children": [
                            {
                                "object": "block",
                                "type": "paragraph",
                                "paragraph": {
                                    "rich_text": [{"type": "text", "text": {"content": transcript}}]
                                }
                            }
                        ]
                    }
                }
            ])
        
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
                                "content": f"Meeting Notes - {data.get('title', 'Untitled Meeting')}"
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

if __name__ == "__main__":
    # Use environment variables for production deployment
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_ENV") == "development"
    
    print(f"Starting Whisper API on {host}:{port}")
    app.run(host=host, port=port, debug=debug) 