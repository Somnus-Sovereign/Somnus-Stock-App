# --- Project Configuration ---
# This file serves as the central configuration for the SLQ project.
# Instead of static YAML, we use Python for dynamic and flexible settings.

import os
from dotenv import load_dotenv

# Load environment variables from .env file in the secrets/ directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'secrets', '.env'))

# --- Model Configuration ---
# Path to the local SLM model file (GGUF format)
# Falls back to a default name if not set in the .env file
MODEL_PATH = os.getenv("MODEL_PATH", "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")

# --- Data Configuration ---
DATA_SOURCES = {
    "yfinance": {
        "enabled": True,
    },
    "alpha_vantage": {
        "enabled": True,
        "api_key": os.getenv("ALPHA_VANTAGE_API_KEY")
    }
}

# --- Backtesting Configuration ---
BACKTEST_SETTINGS = {
    "start_date": "2020-01-01",
    "end_date": "2025-01-01",
    "slippage_bps": 6,
    "commission_bps": 2,
    "initial_capital": 100000
}

# You can add more complex, dynamic configurations here
# For example, feature lists that change based on the model being used.

def get_active_features():
    # Example of a dynamic configuration function
    base_features = ["returns", "rsi_14", "volatility_20"]
    if "NBEATS" in MODEL_PATH:
        base_features.extend(["time_index", "day_of_week"])
    return base_features

FEATURES_CONFIG = {
    "default": get_active_features()
}
