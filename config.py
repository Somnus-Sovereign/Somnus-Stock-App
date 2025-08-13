# /config.py
"""
Central configuration file for the Somnus Stock App.

This file contains settings for data ingestion, feature engineering,
modeling, and backtesting. Using a Python-based config allows for
more dynamic and complex configurations.
"""

from pathlib import Path

# --- Core Paths ---
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXPERIMENTS_DIR = BASE_DIR / "experiments"
LOGS_DIR = BASE_DIR / "logs"

# --- Data Ingestion ---
# A small universe of equities for the MVP
TICKER_UNIVERSE = ["SPY", "QQQ", "AAPL", "MSFT", "GOOG"]

# Data source settings
DATA_SOURCE = "yfinance"

# --- Feature Engineering ---
FEATURE_CONFIG = {
    "returns": {"lags": [1, 5, 10, 21]},
    "rsi": {"window": 14},
    "rolling_skew": {"window": 21},
    "volatility": {"window": 21},
}

# --- Modeling ---
MODEL_CONFIG = {
    "name": "LightGBM",
    "params": {
        "objective": "binary",
        "metric": "binary_logloss",
        "boosting_type": "gbdt",
        "n_estimators": 200,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "max_depth": -1,
        "seed": 42,
        "n_jobs": -1,
        "verbose": -1,
    },
    "target_variable": "target_up_down",
    "prediction_horizon": 1, # predict next day
}

# --- Backtesting ---
BACKTEST_CONFIG = {
    "start_date": "2018-01-01",
    "end_date": "2023-12-31",
    "train_period_years": 3,
    "test_period_months": 6,
    "slippage_bps": 2.0, # 2 basis points
    "commission_bps": 1.5, # 1.5 basis points
}

# --- TUI ---
TUI_CONFIG = {
    "color_scheme": {
        "primary": "bold #FF00FF", # Magenta
        "secondary": "bold #0000FF", # Blue
        "accent": "bold #FF0000", # Red
    },
    "banner_text": "Somnus Quant Copilot",
}
