import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader

from src.backtesting.engine import Backtester
from src.modeling.models.lightgbm_model import LightGBMModel

def calculate_sharpe_ratio(returns, risk_free_rate=0):
    """Calculates the Sharpe ratio."""
    return (returns.mean() - risk_free_rate) / returns.std() * np.sqrt(252)

def calculate_max_drawdown(cumulative_returns):
    """Calculates the maximum drawdown."""
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns - peak) / peak
    return drawdown.min()

def generate_html_report(backtest_results: pd.DataFrame, ticker: str, output_path: str):
    """Generates an HTML report of the backtest results."""

    # Calculate metrics
    returns = backtest_results['strategy_returns']
    cumulative_returns = backtest_results['cumulative_strategy_returns']

    sharpe_ratio = calculate_sharpe_ratio(returns)
    max_drawdown = calculate_max_drawdown(cumulative_returns)
    annualized_return = returns.mean() * 252

    # Create plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cumulative_returns.index, y=cumulative_returns, mode='lines', name='Strategy'))
    fig.update_layout(title=f'Equity Curve for {ticker}', xaxis_title='Date', yaxis_title='Cumulative Returns')
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Render HTML
    env = Environment(loader=FileSystemLoader(str(Path(__file__).parent)))
    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Backtest Report for {{ ticker }}</title>
        <style> body { font-family: sans-serif; } </style>
    </head>
    <body>
        <h1>Backtest Report for {{ ticker }}</h1>
        <h2>Metrics</h2>
        <ul>
            <li>Annualized Return: {{ "%.2f"|format(annualized_return * 100) }}%</li>
            <li>Sharpe Ratio: {{ "%.2f"|format(sharpe_ratio) }}</li>
            <li>Max Drawdown: {{ "%.2f"|format(max_drawdown * 100) }}%</li>
        </ul>
        <h2>Equity Curve</h2>
        {{ plot_html|safe }}
    </body>
    </html>
    """
    template = env.from_string(template_str)

    html = template.render(
        ticker=ticker,
        annualized_return=annualized_return,
        sharpe_ratio=sharpe_ratio,
        max_drawdown=max_drawdown,
        plot_html=plot_html
    )

    with open(output_path, 'w') as f:
        f.write(html)
    print(f"Report saved to {output_path}")

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

    backtester = Backtester(model.model, df)
    results = backtester.run()

    report_path = f"experiments/{ticker}_report.html"
    generate_html_report(results, ticker, report_path)
