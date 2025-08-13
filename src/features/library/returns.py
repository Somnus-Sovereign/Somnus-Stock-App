import pandas as pd

def calculate_returns(df: pd.DataFrame, lags: list[int]) -> pd.DataFrame:
    """
    Calculates lagged returns for the 'Close' price.

    Args:
        df (pd.DataFrame): DataFrame with a 'Close' column.
        lags (list[int]): A list of integer lags for which to calculate returns.

    Returns:
        pd.DataFrame: The original DataFrame with added return columns.
    """
    for lag in lags:
        df[f'return_{lag}d'] = df['Close'].pct_change(periods=lag)
    return df
