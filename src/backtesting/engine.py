import pandas as pd
import numpy as np
from pathlib import Path
import joblib

from src.modeling.models.lightgbm_model import LightGBMModel
from src.features.library.indicators import (
    calculate_returns,
    calculate_volatility,
    calculate_rsi,
    calculate_rolling_skew,
    get_day_of_week,
)

class Backtester:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.results = None

    def run(self):
        """Runs the backtest."""
        # Feature Engineering
        self.data['returns'] = calculate_returns(self.data)
        self.data['volatility'] = calculate_volatility(self.data)
        self.data['rsi'] = calculate_rsi(self.data)
        self.data['skew'] = calculate_rolling_skew(self.data)
        self.data['day_of_week'] = get_day_of_week(self.data)

        self.data.dropna(inplace=True)

        X = self.data[['returns', 'volatility', 'rsi', 'skew', 'day_of_week']]

        # Make predictions
        predictions = self.model.predict(X)
        self.data['prediction'] = predictions

        # Calculate strategy returns
        # Long only: if prediction is 1, hold the stock. If 0, be in cash.
        # The return is the next day's return.
        self.data['strategy_returns'] = np.where(self.data['prediction'].shift(1) == 1, self.data['returns'], 0)

        # Calculate cumulative returns
        self.data['cumulative_strategy_returns'] = (1 + self.data['strategy_returns']).cumprod()

        self.results = self.data
        return self.results

    def plot_equity_curve(self):
        """Plots the equity curve."""
        if self.results is None:
            print("Please run the backtest first.")
            return
        self.results['cumulative_strategy_returns'].plot(title="Equity Curve")
        import matplotlib.pyplot as plt
        plt.show()

if __name__ == '__main__':
    # Load model and data
    ticker = "AAPL"
    model_path = f"experiments/{ticker}_model.pkl"
    data_path = f"data/processed/symbol={ticker}/interval=1d/data.parquet"

    model = LightGBMModel()
    model.load(model_path)

    df = pd.read_parquet(data_path)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # For backtesting, we should use the whole dataset
    # The model was trained on a subset, here we test on the whole period
    # A more realistic scenario would be to use out-of-sample data

    backtester = Backtester(model.model, df)
    results = backtester.run()

    print(results[['returns', 'prediction', 'strategy_returns', 'cumulative_strategy_returns']].head(20))
    print(results[['returns', 'prediction', 'strategy_returns', 'cumulative_strategy_returns']].tail(20))

    # The plot will not work in this environment, but the code is there.
    # backtester.plot_equity_curve()
