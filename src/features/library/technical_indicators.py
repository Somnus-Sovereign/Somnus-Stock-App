import pandas as pd
import numpy as np

def calculate_rsi(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Calculates the Relative Strength Index (RSI).

    Args:
        df (pd.DataFrame): DataFrame with a 'Close' column.
        window (int): The RSI calculation window.

    Returns:
        pd.DataFrame: The original DataFrame with an added RSI column.
    """
    delta = df['Close'].diff()

    # Use clip to separate gains and losses while preserving the initial NaN
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Use rolling mean. min_periods=window is the default but explicit is clearer.
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    # Calculate Relative Strength
    rs = avg_gain / avg_loss

    # Calculate RSI
    # The formula handles the case where avg_loss is 0 (rs is inf), resulting in RSI of 100.
    df[f'rsi_{window}d'] = 100 - (100 / (1 + rs))
    return df

def calculate_rolling_skew(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Calculates the rolling skewness of daily returns.

    Args:
        df (pd.DataFrame): DataFrame with a 'Close' column.
        window (int): The rolling window size.

    Returns:
        pd.DataFrame: The original DataFrame with an added skewness column.
    """
    daily_returns = df['Close'].pct_change()
    df[f'skew_{window}d'] = daily_returns.rolling(window=window).skew()
    return df
