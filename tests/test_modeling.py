import pandas as pd
import numpy as np
import pytest
from pathlib import Path

from src.modeling.models.lightgbm_model import LightGBMModel

@pytest.fixture
def synthetic_data():
    """Creates synthetic data for model testing."""
    X = pd.DataFrame(np.random.rand(100, 5), columns=[f'f{i}' for i in range(5)])
    y = pd.Series(np.random.randint(0, 2, 100))
    return X, y

def test_lightgbm_model_fit_predict(synthetic_data):
    X, y = synthetic_data
    model = LightGBMModel()
    model.fit(X, y)
    predictions = model.predict(X)
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(y)

def test_lightgbm_model_save_load(synthetic_data, tmp_path):
    X, y = synthetic_data
    model = LightGBMModel()
    model.fit(X, y)

    model_path = tmp_path / "test_model.pkl"
    model.save(model_path)
    assert model_path.exists()

    new_model = LightGBMModel()
    new_model.load(model_path)

    predictions = new_model.predict(X)
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(y)
