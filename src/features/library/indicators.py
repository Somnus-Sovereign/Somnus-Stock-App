import pandas as pd
import numpy as np

def calculate_returns(df: pd.DataFrame, window: int = 1) -> pd.Series:
    """Calculates the n-period return of the 'Close' price."""
    return df['Close'].pct_change(periods=window)

def calculate_volatility(df: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculates the rolling volatility of returns."""
    returns = df['Close'].pct_change()
    return returns.rolling(window=window).std()

def calculate_rsi(df: pd.DataFrame, window: int = 14) -> pd.Series:
    """Calculates the Relative Strength Index (RSI)."""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_rolling_skew(df: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculates the rolling skewness of returns."""
    returns = df['Close'].pct_change()
    return returns.rolling(window=window).skew()

def get_day_of_week(df: pd.DataFrame) -> pd.Series:
    """Returns the day of the week for each row."""
    return pd.Series(df.index.dayofweek, index=df.index)

if __name__ == '__main__':
    # Create a sample DataFrame for testing
    dates = pd.to_datetime(pd.date_range(start='2023-01-01', periods=100))
    close_prices = pd.Series(np.random.randn(100).cumsum() + 100, index=dates)
    data = pd.DataFrame({'Close': close_prices})

    # Calculate features
    data['returns'] = calculate_returns(data)
    data['volatility'] = calculate_volatility(data)
    data['rsi'] = calculate_rsi(data)
    data['skew'] = calculate_rolling_skew(data)
    data['day_of_week'] = get_day_of_week(data)

    print(data.head(20))
    print(data.tail(20))
