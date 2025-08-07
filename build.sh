#!/bin/bash

# Install system dependencies for Whisper
echo "Installing system dependencies..."

# Update package list
apt-get update

# Install ffmpeg and other required packages
apt-get install -y ffmpeg
apt-get install -y libsndfile1
apt-get install -y libportaudio2
apt-get install -y portaudio19-dev

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!" 