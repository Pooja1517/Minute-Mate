#!/bin/bash

echo "Starting minimal build for Render..."

# Update package list
apt-get update

# Install only essential system dependencies
echo "Installing ffmpeg..."
apt-get install -y ffmpeg

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install Python dependencies with minimal requirements
echo "Installing Python dependencies..."
pip install --upgrade setuptools wheel
pip install -r requirements-render-minimal.txt --no-cache-dir

echo "Minimal build completed successfully!" 