#!/bin/bash

echo "======================================"
echo "Insurance Claim System - Setup Script"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "📦 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ All dependencies installed!"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo ""
    echo "Please create a .env file with your OpenAI API key:"
    echo "  echo 'OPENAI_API_KEY=your-key-here' > .env"
    echo ""
else
    echo "✅ .env file exists"
fi

echo ""
echo "======================================"
echo "Setup complete! 🎉"
echo "======================================"
echo ""
echo "To run the system:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
