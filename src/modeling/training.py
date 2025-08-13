import pandas as pd
import numpy as np
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
import sys
import os
from dateutil.relativedelta import relativedelta

# --- Project Imports ---
from config import (
    PROCESSED_DATA_DIR,
    EXPERIMENTS_DIR,
    TICKER_UNIVERSE,
    FEATURE_CONFIG,
    MODEL_CONFIG,
    BACKTEST_CONFIG
)
from src.features.library.returns import calculate_returns
from src.features.library.volatility import calculate_volatility
from src.features.library.technical_indicators import calculate_rsi, calculate_rolling_skew
from src.features.library.calendar import add_day_of_week
from src.modeling.models.lightgbm_model import LightGBMModel

# --- Initialization ---
console = Console()

def load_data(ticker: str, interval: str = '1D') -> pd.DataFrame | None:
    """Loads a single Parquet file for a given ticker and interval."""
    filepath = PROCESSED_DATA_DIR / f"symbol={ticker}" / f"interval={interval.upper()}" / "data.parquet"
    if not filepath.exists():
        console.log(f"[bold red]Error: Data file not found at {filepath}[/bold red]")
        return None
    return pd.read_parquet(filepath)

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Applies all feature engineering steps."""
    df = calculate_returns(df, lags=FEATURE_CONFIG['returns']['lags'])
    df = calculate_volatility(df, window=FEATURE_CONFIG['volatility']['window'])
    df = calculate_rsi(df, window=FEATURE_CONFIG['rsi']['window'])
    df = calculate_rolling_skew(df, window=FEATURE_CONFIG['rolling_skew']['window'])
    df = add_day_of_week(df)
    return df

def create_target(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """Creates the binary target variable."""
    df['target'] = (df['Close'].shift(-horizon) > df['Close']).astype(int)
    return df

def get_walk_forward_splits(start_date, end_date, train_period, test_period):
    """Generates date ranges for walk-forward validation."""
    train_start = pd.to_datetime(start_date)
    while True:
        train_end = train_start + train_period
        test_start = train_end
        test_end = test_start + test_period

        if test_end > pd.to_datetime(end_date):
            break

        yield train_start, train_end, test_start, test_end

        train_start = train_start + test_period

@click.command()
@click.option('--ticker', default='SPY', help='Ticker symbol to train on.', type=click.Choice(TICKER_UNIVERSE))
def main(ticker: str):
    """
    Main training pipeline for a single asset.
    Orchestrates data loading, feature engineering, walk-forward validation,
    model training, and prediction.
    """
    console.rule(f"[bold blue]Starting Modeling Pipeline for {ticker}[/bold blue]")

    # --- Debug: Print experiment directory ---
    console.log(f"DEBUG: Experiments directory is: {EXPERIMENTS_DIR.resolve()}")
    # -----------------------------------------

    # 1. Load Data
    console.log("1. Loading data...")
    df = load_data(ticker)
    if df is None:
        return

    # Sanitize column names by removing the ticker suffix from yfinance
    df.columns = [col.replace(f'_{ticker}', '') for col in df.columns]

    # 2. Build Features
    console.log("2. Building features...")
    df = build_features(df)

    # 3. Create Target
    console.log("3. Creating target variable...")
    df = create_target(df, horizon=MODEL_CONFIG['prediction_horizon'])

    # Drop rows with NaNs created by feature engineering and target creation
    df.dropna(inplace=True)

    features = [col for col in df.columns if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'target']]
    X = df[features]
    y = df['target']

    # 4. Walk-Forward Validation
    console.log("4. Starting walk-forward validation...")

    train_period = relativedelta(years=BACKTEST_CONFIG['train_period_years'])
    test_period = relativedelta(months=BACKTEST_CONFIG['test_period_months'])

    splits = get_walk_forward_splits(
        df.index.min().strftime('%Y-%m-%d'),
        df.index.max().strftime('%Y-%m-%d'),
        train_period,
        test_period
    )

    all_predictions = []

    for i, (train_start, train_end, test_start, test_end) in enumerate(splits):
        fold_id = f"fold_{i+1}_{train_start.date()}_{test_end.date()}"
        console.rule(f"Processing {fold_id}")

        # Select data for the current fold
        X_train = X.loc[train_start:train_end]
        y_train = y.loc[train_start:train_end]
        X_test = X.loc[test_start:test_end]
        y_test = y.loc[test_start:test_end]

        console.log(f"Train: {X_train.index.min().date()} to {X_train.index.max().date()} ({len(X_train)} rows)")
        console.log(f"Test:  {X_test.index.min().date()} to {X_test.index.max().date()} ({len(X_test)} rows)")

        # Train model
        model = LightGBMModel(params=MODEL_CONFIG['params'])
        model.fit(X_train, y_train)

        # Make predictions
        preds = model.predict(X_test)

        fold_results = pd.DataFrame({'prediction': preds, 'actual': y_test})
        all_predictions.append(fold_results)

        # Save model and feature importances
        experiment_dir = EXPERIMENTS_DIR / ticker / fold_id
        experiment_dir.mkdir(parents=True, exist_ok=True)
        model_path = experiment_dir / "model.joblib"
        console.log(f"DEBUG: Saving model to: {model_path.resolve()}")
        model.save(model_path)

        feature_importances = model.feature_importances_
        feature_importances.to_csv(experiment_dir / "feature_importances.csv", index=False)

    # 5. Save Results
    console.log("\n5. Saving out-of-sample predictions...")
    if all_predictions:
        oos_predictions = pd.concat(all_predictions)
        output_path = EXPERIMENTS_DIR / f"{ticker}_oos_predictions.csv"
        console.log(f"DEBUG: Saving predictions to: {output_path.resolve()}")
        oos_predictions.to_csv(output_path)
        console.log(f"Predictions saved to [green]{output_path}[/green]")
    else:
        console.log("[yellow]No walk-forward folds were processed. Check date ranges in config.[/yellow]")

    console.rule(f"[bold green]Modeling Pipeline for {ticker} Complete[/bold green]")


if __name__ == "__main__":
    main()
