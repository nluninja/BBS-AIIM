#!/bin/bash

# Startup script for BBS Travel Assistant Web UI

echo "🏖️ Starting BBS Travel Assistant Web UI..."

# Check if virtual environment exists
if [ ! -d "myagent" ]; then
    echo "❌ Virtual environment 'myagent' not found!"
    echo "Please run setup first:"
    echo "  python3 -m venv myagent"
    echo "  source myagent/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your Google API key:"
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your GOOGLE_API_KEY"
    exit 1
fi

# Activate virtual environment and run Streamlit
echo "🚀 Activating environment and starting web UI..."
source myagent/bin/activate
streamlit run app.py --server.port 8501 --server.address localhost