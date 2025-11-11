#!/bin/bash

echo "🚀 AI Video Quiz Generator - Quick Start Script"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "⚙️  Please edit .env and add your OpenAI API key"
    exit 1
fi

# Create necessary directories
mkdir -p uploads outputs

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "1. In terminal 1: python app.py"
echo "2. In terminal 2: streamlit run streamlit_app.py"
echo ""
