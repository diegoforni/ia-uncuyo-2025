#!/bin/bash
# Script to set up Python virtual environment and install dependencies for TP3
set -e
python3 -m venv .venv
echo "Activating virtual environment"
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed successfully."
