# src/ingestion/yfinance_connector.py
import yfinance as yf
import pandas as pd
from pathlib import Path
import click
from rich.console import Console
import sys
import os

# Adjust the Python path to allow importing from the root 'src' directory
# This is a common pattern for standalone scripts in a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config import PROCESSED_DATA_DIR, TICKER_UNIVERSE, BACKTEST_CONFIG

console = Console()

def download_data(ticker: str, interval: str, start_date: str = None, end_date: str = None, period: str = None) -> pd.DataFrame | None:
    """
    Downloads historical market data for a given ticker and interval.

    Args:
        ticker (str): The stock ticker symbol.
        interval (str): The data interval (e.g., '1d', '1m').
        start_date (str, optional): The start date for the data (YYYY-MM-DD). Defaults to None.
        end_date (str, optional): The end date for the data (YYYY-MM-DD). Defaults to None.
        period (str, optional): The period over which to fetch data (e.g., '7d'). Defaults to None.

    Returns:
        pd.DataFrame | None: A DataFrame containing the downloaded data, or None if download fails.
    """
    try:
        console.log(f"Downloading {interval} data for [bold cyan]{ticker}[/]...")
        data = yf.download(
            tickers=ticker,
            start=start_date,
            end=end_date,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )
        if data.empty:
            console.log(f"[yellow]No data found for {ticker} for the given parameters.[/yellow]")
            return None

        # Flatten MultiIndex columns if they exist (e.g., from yfinance)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = ['_'.join(col).strip('_') for col in data.columns.values]

        data.index.name = 'timestamp'
        return data
    except Exception as e:
        console.log(f"[bold red]Error downloading data for {ticker}: {e}[/bold red]")
        return None

def save_data_to_parquet(data: pd.DataFrame, ticker: str, interval: str):
    """
    Saves a DataFrame to a partitioned Parquet file structure.

    Args:
        data (pd.DataFrame): The data to save.
        ticker (str): The stock ticker symbol.
        interval (str): The data interval (e.g., '1D', '1M').
    """
    # Use interval notation like '1D' or '1M' for directory names
    interval_str = interval.upper()
    output_dir = PROCESSED_DATA_DIR / f"symbol={ticker}" / f"interval={interval_str}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "data.parquet"
    data.to_parquet(output_path)
    console.log(f"Data for [bold cyan]{ticker}[/] ({interval_str}) saved to [green]{output_path}[/green]")

@click.command()
@click.option('--full-history', is_flag=True, help="Fetch full daily history instead of the backtest period from config.")
def main(full_history: bool):
    """
    Main function to ingest data for all tickers in the universe.
    This script will fetch historical data from yfinance and save it locally
    in Parquet format.
    """
    console.rule("[bold blue]Starting Data Ingestion[/bold blue]")

    start_date = None if full_history else BACKTEST_CONFIG['start_date']
    end_date = None if full_history else BACKTEST_CONFIG['end_date']

    for ticker in TICKER_UNIVERSE:
        # --- Download Daily Data ---
        daily_data = download_data(ticker, interval='1d', start_date=start_date, end_date=end_date)
        if daily_data is not None:
            save_data_to_parquet(daily_data, ticker, '1d')

        # --- Download 1-Minute Data ---
        # yfinance typically limits 1m data to the last 7 days.
        console.log("[yellow]Note: 1-minute data is typically limited to the last 7 days by the yfinance API.[/yellow]")
        minute_data = download_data(ticker, interval='1m', period='7d')
        if minute_data is not None:
            save_data_to_parquet(minute_data, ticker, '1m')

    console.rule("[bold green]Data Ingestion Complete[/bold green]")

if __name__ == "__main__":
    main()
