#!/usr/bin/env bash
# run.sh — DocToExam launcher (Linux / Mac)
# Double-click or run: bash run.sh

cd "$(dirname "$0")"

# Check Python 3 exists
if ! command -v python3 &>/dev/null; then
    echo "❌  Python 3 not found. Please install Python 3.9+."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦  Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install / upgrade dependencies
echo "📦  Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "🚀  Starting DocToExam..."
echo ""
python main.py
