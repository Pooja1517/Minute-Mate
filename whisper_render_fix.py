from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import logging
import time
import gc

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
        # Force garbage collection before loading models
        gc.collect()
        
        # Try to use faster-whisper first (more memory efficient)
        try:
            from faster_whisper import WhisperModel
            model_name = os.getenv("WHISPER_MODEL", "tiny")
            logger.info(f"Loading faster-whisper model: {model_name}")
            
            # Use CPU and small model for Render free tier with minimal memory usage
            whisper_model = WhisperModel(
                model_name, 
                device="cpu", 
                compute_type="int8",
                cpu_threads=1,
                num_workers=1,
                download_root="/tmp"  # Use temp directory
            )
            model_type = "faster-whisper"
            logger.info("Faster-whisper model loaded successfully!")
            return True
            
        except ImportError:
            logger.info("faster-whisper not available, trying regular whisper...")
            # Fallback to regular whisper if faster-whisper not available
            import whisper
            model_name = os.getenv("WHISPER_MODEL", "tiny")
            logger.info(f"Loading regular whisper model: {model_name}")
            
            # Set environment variables to minimize memory usage
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            
            whisper_model = whisper.load_model(model_name, download_root="/tmp")
            model_type = "regular-whisper"
            logger.info("Regular whisper model loaded successfully!")
            return True
            
    except Exception as e:
        logger.error(f"Error loading Whisper model: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {str(e)}")
        return False

# Load models on startup
@app.before_first_request
def initialize_models():
    """Load models before first request"""
    logger.info("Initializing Whisper models...")
    if not load_models():
        logger.error("Failed to load Whisper models!")
    else:
        logger.info("Whisper models loaded successfully!")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    if whisper_model is not None:
        return jsonify({
            "status": "healthy",
            "whisper_model": "loaded",
            "message": "Service is running",
            "model_type": model_type,
            "endpoints": {
                "health": "/health",
                "transcribe": "/transcribe"
            }
        })
    else:
        return jsonify({
            "status": "unhealthy",
            "whisper_model": "not_loaded",
            "message": "Models not loaded",
            "endpoints": {
                "health": "/health",
                "transcribe": "/transcribe"
            }
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
        
        if model_type == "faster-whisper":
            # Use faster-whisper transcription
            segments, info = whisper_model.transcribe(
                temp_path,
                language="en",
                beam_size=1,
                best_of=1,
                temperature=0.0,
                compression_ratio_threshold=2.4,
                log_prob_threshold=-1.0,
                no_speech_threshold=0.6,
                condition_on_previous_text=False,
                initial_prompt=None,
                word_timestamps=False,
                prepend_punctuations="\"'"¿([{-",
                append_punctuations="\"'.。,，!！?？:：")]}、"
            )
            
            # Extract text from segments
            transcript_text = " ".join([segment.text for segment in segments])
            
        else:
            # Use regular whisper transcription
            result = whisper_model.transcribe(
                temp_path,
                language="en",
                task="transcribe",
                fp16=False,  # Force FP32 for CPU
                verbose=False
            )
            transcript_text = result["text"]
        
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except:
            pass
        
        transcription_time = time.time() - start_time
        logger.info(f"Transcription completed in {transcription_time:.2f}s: {len(transcript_text)} characters")
        
        return jsonify({
            "text": transcript_text,
            "language": "en",
            "processing_time": f"{transcription_time:.2f}s",
            "model_type": model_type
        })
        
    except Exception as e:
        # Clean up temporary file on error
        try:
            if 'temp_path' in locals():
                os.unlink(temp_path)
        except:
            pass
        
        logger.error(f"Transcription error: {e}")
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
    # Load models immediately when running directly
    logger.info("Starting Whisper API...")
    if load_models():
        logger.info("Starting Whisper API on 127.0.0.1:5001")
        app.run(host="127.0.0.1", port=5001, debug=False)
    else:
        logger.error("Failed to load models. Cannot start service.")
        exit(1) 