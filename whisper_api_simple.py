from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for models
whisper_model = None

def load_models():
    """Load only essential models to fit in Render free tier memory"""
    global whisper_model
    
    try:
        # Load only Whisper tiny model (39MB)
        model_name = os.getenv("WHISPER_MODEL", "tiny")
        logger.info(f"Loading Whisper model: {model_name}")
        whisper_model = whisper.load_model(model_name)
        logger.info("Whisper model loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading Whisper model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if whisper_model is not None:
        return jsonify({
            "status": "healthy",
            "whisper_model": "loaded",
            "message": "Service is running"
        })
    else:
        return jsonify({
            "status": "unhealthy",
            "whisper_model": "not_loaded",
            "message": "Models not loaded"
        }), 500

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio file"""
    if whisper_model is None:
        return jsonify({"error": "Whisper model not loaded"}), 500
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No audio file selected"}), 400
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
        
        # Transcribe using Whisper
        logger.info("Starting transcription...")
        result = whisper_model.transcribe(temp_path)
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        transcript = result["text"]
        logger.info(f"Transcription completed: {len(transcript)} characters")
        
        return jsonify({
            "transcript": transcript,
            "language": result.get("language", "unknown"),
            "model_used": os.getenv("WHISPER_MODEL", "tiny")
        })
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "message": "Minute Mate Whisper API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "transcribe": "/transcribe"
        }
    })

if __name__ == "__main__":
    # Load models before starting server
    if load_models():
        host = os.getenv("HOST", "127.0.0.1")
        port = int(os.getenv("PORT", 5001))
        debug = os.getenv("FLASK_ENV") == "development"
        
        logger.info(f"Starting Whisper API on {host}:{port}")
        app.run(host=host, port=port, debug=debug)
    else:
        logger.error("Failed to load models. Exiting...")
        exit(1) 