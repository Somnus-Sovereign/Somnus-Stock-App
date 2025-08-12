import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from src.modeling.models.lightgbm_model import LightGBMModel
from src.features.library.indicators import (
    calculate_returns,
    calculate_volatility,
    calculate_rsi,
    calculate_rolling_skew,
    get_day_of_week,
)

def train_single_stock(ticker: str):
    """
    Trains a model for a single stock.
    """
    print(f"Training model for {ticker}...")

    # Load data
    data_path = f"data/processed/symbol={ticker}/interval=1d/data.parquet"
    if not Path(data_path).exists():
        print(f"Data for {ticker} not found. Please run the ingestion script first.")
        return

    df = pd.read_parquet(data_path)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # Feature Engineering
    df['returns'] = calculate_returns(df)
    df['volatility'] = calculate_volatility(df)
    df['rsi'] = calculate_rsi(df)
    df['skew'] = calculate_rolling_skew(df)
    df['day_of_week'] = get_day_of_week(df)

    # Target variable
    df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    # Drop NaNs
    df.dropna(inplace=True)

    if df.empty:
        print(f"Not enough data for {ticker} after feature calculation.")
        return

    # Split data
    X = df[['returns', 'volatility', 'rsi', 'skew', 'day_of_week']]
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    if len(X_train) == 0 or len(X_test) == 0:
        print(f"Not enough data for {ticker} to train/test.")
        return

    # Train model
    model = LightGBMModel()
    model.fit(X_train, y_train)

    # Evaluate model
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

    # Save model
    model_path = f"experiments/{ticker}_model.pkl"
    model.save(model_path)
    print(f"Model for {ticker} saved to {model_path}")


if __name__ == '__main__':
    train_single_stock("AAPL")
