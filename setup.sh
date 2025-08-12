#!/bin/bash
# This script sets up the Python virtual environment and installs dependencies.

# Note for Windows users: You can run this script using Git Bash or the
# Windows Subsystem for Linux (WSL). Alternatively, you can execute
# the commands manually in Command Prompt or PowerShell:
#
# py -3 -m venv .venv
# .venv\Scripts\activate
# pip install -r requirements.txt

echo "Creating Python virtual environment in ./.venv/ ..."
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

echo "Installing dependencies from requirements.txt ..."
pip install -r requirements.txt

echo ""
echo "Setup complete. Run 'source .venv/bin/activate' to start working."
