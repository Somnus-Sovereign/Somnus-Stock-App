import pandas as pd

def add_day_of_week(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds the day of the week as a feature (Monday=0, Sunday=6).

    Args:
        df (pd.DataFrame): DataFrame with a DatetimeIndex.

    Returns:
        pd.DataFrame: The original DataFrame with an added 'day_of_week' column.
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a DatetimeIndex.")
    df['day_of_week'] = df.index.dayofweek
    return df
