# PowerShell setup script for Windows users
# This script creates a Python virtual environment and installs dependencies.

Write-Host "Creating Python virtual environment in ./.venv/ ..."
python -m venv .venv

Write-Host "Activating virtual environment ..."
.\.venv\Scripts\Activate.ps1

Write-Host "Installing dependencies from requirements.txt ..."
pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete. Run '.\.venv\Scripts\Activate.ps1' to start working."
