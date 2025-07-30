import os
os.environ["PATH"] += os.pathsep + r"C:\Users\T1IN\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

from flask import Flask, request, jsonify
import whisper
import tempfile
from transformers import pipeline
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model = whisper.load_model("small")  # or "base", "medium", "large"

# Load summarization model once at startup
# Use a smaller, faster summarization model for low-resource systems
# Use a tiny summarization model for speed and compatibility
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

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

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    transcript = data.get('transcript', '')
    print("Received transcript:", transcript)
    if not transcript:
        print("No transcript provided.")
        return jsonify({"error": "No transcript provided"}), 400
    try:
        # Prompt the summarizer for bullet points and decisions
        prompt = "Summarize the following meeting transcript as bullet points, including key decisions if any:\n" + transcript
        summary = summarizer(prompt, max_length=80, min_length=10, do_sample=False)[0]['summary_text']
        print("Summary:", summary)
        if not summary.strip():
            summary = "No summary could be generated for this transcript."
        action_items = extract_action_items(transcript)
        print("Action Items:", action_items)
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
    app.run(host="0.0.0.0", port=5001, debug=True) 