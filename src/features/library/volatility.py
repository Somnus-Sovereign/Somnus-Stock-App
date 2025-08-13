import pandas as pd

def calculate_volatility(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Calculates the rolling volatility of daily returns.

    Args:
        df (pd.DataFrame): DataFrame with a 'Close' column.
        window (int): The rolling window size in days.

    Returns:
        pd.DataFrame: The original DataFrame with an added volatility column.
    """
    # Calculate daily returns first
    daily_returns = df['Close'].pct_change()
    # Calculate rolling standard deviation of returns
    df[f'volatility_{window}d'] = daily_returns.rolling(window=window).std() * (252**0.5)
    # Annualize the volatility
    return df
