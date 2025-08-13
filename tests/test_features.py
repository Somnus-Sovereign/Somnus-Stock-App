import pytest
import pandas as pd
import numpy as np

# Adjust path to import from src
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.features.library.returns import calculate_returns
from src.features.library.volatility import calculate_volatility
from src.features.library.technical_indicators import calculate_rsi, calculate_rolling_skew
from src.features.library.calendar import add_day_of_week

@pytest.fixture
def sample_ohlcv_data() -> pd.DataFrame:
    """Creates a sample DataFrame with OHLCV data for testing."""
    dates = pd.to_datetime(pd.date_range(start="2023-01-01", periods=30, freq='D'))
    close_prices = np.linspace(100, 150, 30) + np.random.normal(0, 2, 30)
    data = pd.DataFrame({
        'Open': close_prices - 1,
        'High': close_prices + 2,
        'Low': close_prices - 2,
        'Close': close_prices,
        'Volume': np.random.randint(10000, 50000, 30)
    }, index=dates)
    data.index.name = 'timestamp'
    return data

def test_calculate_returns(sample_ohlcv_data):
    """Tests the calculate_returns function."""
    df = sample_ohlcv_data.copy()
    lags = [1, 5]
    df = calculate_returns(df, lags)

    assert 'return_1d' in df.columns
    assert 'return_5d' in df.columns
    assert pd.isna(df['return_1d'].iloc[0])
    assert pd.isna(df['return_5d'].iloc[4])

    # Check a known value
    expected_return_1d = (df['Close'].iloc[1] / df['Close'].iloc[0]) - 1
    assert np.isclose(df['return_1d'].iloc[1], expected_return_1d)

def test_calculate_volatility(sample_ohlcv_data):
    """Tests the calculate_volatility function."""
    df = sample_ohlcv_data.copy()
    window = 21
    df = calculate_volatility(df, window)

    assert f'volatility_{window}d' in df.columns
    # The first value is at index `window`, so `window` NaNs total
    assert df[f'volatility_{window}d'].isna().sum() == window

def test_calculate_rsi(sample_ohlcv_data):
    """Tests the calculate_rsi function."""
    df = sample_ohlcv_data.copy()
    window = 14
    df = calculate_rsi(df, window)

    assert f'rsi_{window}d' in df.columns
    # diff() creates 1 NaN, rolling() creates window-1 NaNs. Total = window NaNs.
    assert df[f'rsi_{window}d'].iloc[0:window].isna().all()
    assert df[f'rsi_{window}d'].min() >= 0
    assert df[f'rsi_{window}d'].max() <= 100

def test_calculate_rolling_skew(sample_ohlcv_data):
    """Tests the calculate_rolling_skew function."""
    df = sample_ohlcv_data.copy()
    window = 21
    df = calculate_rolling_skew(df, window)

    assert f'skew_{window}d' in df.columns
    # The first value is at index `window`, so `window` NaNs total
    assert df[f'skew_{window}d'].isna().sum() == window

def test_add_day_of_week(sample_ohlcv_data):
    """Tests the add_day_of_week function."""
    df = sample_ohlcv_data.copy()
    df = add_day_of_week(df)

    assert 'day_of_week' in df.columns
    assert df['day_of_week'].iloc[0] == 6 # 2023-01-01 was a Sunday
    assert df['day_of_week'].iloc[1] == 0 # 2023-01-02 was a Monday
    assert pd.api.types.is_integer_dtype(df['day_of_week'])

def test_add_day_of_week_raises_error_on_wrong_index(sample_ohlcv_data):
    """Tests that a TypeError is raised if the index is not a DatetimeIndex."""
    df = sample_ohlcv_data.copy().reset_index() # Remove DatetimeIndex
    with pytest.raises(TypeError):
        add_day_of_week(df)
