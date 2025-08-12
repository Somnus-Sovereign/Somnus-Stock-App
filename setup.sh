#!/bin/bash
# This script sets up the Python virtual environment and installs dependencies.


# Note for Windows users:
# - You can run this script using Git Bash or WSL.
# - For native Windows/PowerShell setup, use the new 'setup.ps1' script provided in this directory.
# - Alternatively, you can execute the following commands manually in PowerShell:
#     python -m venv .venv
#     .\.venv\Scripts\Activate.ps1
#     pip install -r requirements.txt

echo "Creating Python virtual environment in ./.venv/ ..."
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

echo "Installing dependencies from requirements.txt ..."
pip install -r requirements.txt

echo ""
echo "Setup complete. Run 'source .venv/bin/activate' to start working."
