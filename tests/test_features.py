import pandas as pd
import numpy as np
import pytest

from src.features.library.indicators import (
    calculate_returns,
    calculate_volatility,
    calculate_rsi,
    calculate_rolling_skew,
    get_day_of_week,
)

@pytest.fixture
def sample_data():
    """Creates a sample DataFrame for testing."""
    dates = pd.to_datetime(pd.date_range(start='2023-01-01', periods=100))
    close_prices = pd.Series(np.random.randn(100).cumsum() + 100, index=dates)
    data = pd.DataFrame({'Close': close_prices})
    return data

def test_calculate_returns(sample_data):
    returns = calculate_returns(sample_data)
    assert isinstance(returns, pd.Series)
    assert len(returns) == len(sample_data)
    assert pd.isna(returns.iloc[0])

def test_calculate_volatility(sample_data):
    volatility = calculate_volatility(sample_data, window=5)
    assert isinstance(volatility, pd.Series)
    assert len(volatility) == len(sample_data)
    assert volatility.isna().sum() == 5

def test_calculate_rsi(sample_data):
    rsi = calculate_rsi(sample_data, window=14)
    assert isinstance(rsi, pd.Series)
    assert len(rsi) == len(sample_data)
    assert rsi.isna().sum() >= 13
    assert rsi.min() >= 0
    assert rsi.max() <= 100

def test_calculate_rolling_skew(sample_data):
    skew = calculate_rolling_skew(sample_data, window=20)
    assert isinstance(skew, pd.Series)
    assert len(skew) == len(sample_data)
    assert skew.isna().sum() >= 20

def test_get_day_of_week(sample_data):
    dow = get_day_of_week(sample_data)
    assert isinstance(dow, pd.Series)
    assert len(dow) == len(sample_data)
    assert dow.min() >= 0
    assert dow.max() <= 6
