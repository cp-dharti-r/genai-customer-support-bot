#!/bin/bash

echo "🚀 Starting Customer Support Bot - LLM Comparison Tool"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Please copy env.example to .env and configure your API keys."
    echo "   cp env.example .env"
    echo "   Then edit .env with your API keys and run this script again."
    exit 1
fi

# Start the application
echo "🌐 Starting the application..."
echo "📖 API docs will be available at: http://localhost:8000/docs"
echo "💬 Chat interface will be available at: http://localhost:8000/"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python main.py
