#!/bin/bash

# Render-optimized build script for Whisper API
echo "Starting Render-optimized build..."

# Upgrade pip to latest version
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install system dependencies if available (Render may not have apt-get)
if command -v apt-get &> /dev/null; then
    echo "Installing system dependencies..."
    apt-get update
    apt-get install -y ffmpeg libsndfile1
else
    echo "apt-get not available, skipping system dependencies"
    echo "ffmpeg should be available in Render's environment"
fi

# Install Python dependencies with specific order and flags
echo "Installing Python dependencies..."
pip install --upgrade setuptools wheel

# Install faster-whisper first (more memory efficient)
echo "Installing faster-whisper..."
pip install faster-whisper==0.10.0 --no-cache-dir

# Install other dependencies
echo "Installing other dependencies..."
pip install -r requirements-render-optimized.txt --no-cache-dir

echo "Render-optimized build completed successfully!"
echo "Using faster-whisper for memory efficiency"
