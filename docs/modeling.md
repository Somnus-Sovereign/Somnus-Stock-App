# Machine Learning Modeling

The `modeling` module is responsible for training and evaluating machine learning models.

## Model Training

The `src/modeling/training.py` script is the main entry point for training models. This script uses a walk-forward cross-validation approach to train and evaluate models. This approach is more realistic than a simple train-test split, as it simulates how the model would be used in a real-world trading scenario.

## Supported Models

The project is designed to be flexible and support a wide range of modeling techniques. The core modeling stack includes:

*   **Forecasting/Classification:** LightGBM/XGBoost, ARIMA/TBATS, N-BEATS/TFT, DeepAR.
*   **Regime Detection:** Hidden Markov Models, spectral clustering.
*   **Ensembles:** Stacking and blending of different models.

You can easily add new models by creating a new model class in the `src/modeling/models/` directory.

## Model Evaluation

Models are evaluated using a variety of metrics, including:

*   Sharpe Ratio
*   Sortino Ratio
*   Maximum Drawdown
*   Calmar Ratio
*   Hit Rate
*   Average Win/Loss
*   Turnover
*   Exposure Concentration
*   Probability of Ruin

The results of the evaluation are saved in an HTML report in the `experiments/` directory.
