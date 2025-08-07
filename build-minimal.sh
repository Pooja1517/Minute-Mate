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

# Upgrade pip to latest version
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies with minimal versions
echo "Installing minimal Python dependencies..."
pip install --upgrade setuptools wheel
pip install -r requirements-minimal.txt --no-cache-dir

# Install additional packages separately if needed
echo "Installing additional packages..."
pip install notion-client==2.2.1 --no-cache-dir

echo "Build completed successfully!" 