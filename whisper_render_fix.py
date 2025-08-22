from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for models
whisper_model = None
model_type = None

def load_models():
    """Load lightweight Whisper model optimized for Render free tier"""
    global whisper_model, model_type
    
    try:
        # Try to use faster-whisper first (more memory efficient)
        try:
            from faster_whisper import WhisperModel
            model_name = os.getenv("WHISPER_MODEL", "tiny")
            logger.info(f"Loading faster-whisper model: {model_name}")
            
            # Use CPU and small model for Render free tier
            whisper_model = WhisperModel(
                model_name, 
                device="cpu", 
                compute_type="int8",
                cpu_threads=1,
                num_workers=1
            )
            model_type = "faster-whisper"
            logger.info("Faster-whisper model loaded successfully!")
            return True
            
        except ImportError:
            # Fallback to regular whisper if faster-whisper not available
            import whisper
            model_name = os.getenv("WHISPER_MODEL", "tiny")
            logger.info(f"Loading regular whisper model: {model_name}")
            whisper_model = whisper.load_model(model_name)
            model_type = "regular-whisper"
            logger.info("Regular whisper model loaded successfully!")
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
            "message": "Service is running",
            "model_type": model_type
        })
    else:
        return jsonify({
            "status": "unhealthy",
            "whisper_model": "not_loaded",
            "message": "Models not loaded"
        }), 500

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio file with memory optimization"""
    if whisper_model is None:
        return jsonify({"error": "Whisper model not loaded"}), 500
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No audio file selected"}), 400
    
    # Check file size - strict limit for Render free tier
    file_size_mb = len(audio_file.read()) / (1024 * 1024)
    audio_file.seek(0)  # Reset file pointer
    
    if file_size_mb > 3:  # 3MB limit for Render free tier
        return jsonify({"error": f"File too large ({file_size_mb:.1f} MB). Maximum size is 3 MB for Render free tier."}), 400
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
        
        # Transcribe using Whisper with memory optimization
        logger.info("Starting transcription...")
        start_time = time.time()
        
        # Use different transcription method based on model type
        if model_type == "faster-whisper":
            # faster-whisper
            segments, info = whisper_model.transcribe(
                temp_path,
                beam_size=1,  # Minimal beam size for memory
                best_of=1,     # Minimal best_of for memory
                temperature=0.0,  # Deterministic output
                compression_ratio_threshold=2.4,
                log_prob_threshold=-1.0,
                no_speech_threshold=0.6,
                condition_on_previous_text=False,
                initial_prompt=None
            )
            
            # Extract text from segments
            transcript = " ".join([segment.text for segment in segments])
            language = info.language if hasattr(info, 'language') else "unknown"
            
        else:
            # regular whisper - use compatible parameters
            result = whisper_model.transcribe(
                temp_path,
                fp16=False,  # Disable fp16 for better compatibility
                verbose=False,
                condition_on_previous_text=False,
                compression_ratio_threshold=2.4,
                # Remove incompatible parameters for regular whisper
                language=None,
                task="transcribe"
            )
            transcript = result["text"]
            language = result.get("language", "unknown")
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        transcription_time = time.time() - start_time
        logger.info(f"Transcription completed in {transcription_time:.2f}s: {len(transcript)} characters")
        
        return jsonify({
            "text": transcript,
            "language": language,
            "model_used": os.getenv("WHISPER_MODEL", "tiny"),
            "processing_time": round(transcription_time, 2)
        })
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        
        # Clean up on error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception:
                pass
                
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "message": "Minute Mate Whisper API (Render Optimized)",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "transcribe": "/transcribe"
        },
        "optimizations": [
            "Memory-optimized for Render free tier",
            "Uses faster-whisper when available",
            "CPU-only processing",
            "Small model (tiny) by default"
        ]
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