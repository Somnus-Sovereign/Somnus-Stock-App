import yfinance as yf
import pandas as pd
from pathlib import Path

def download_data(tickers: list[str], start_date: str, end_date: str, interval: str = "1d"):
    """
    Downloads historical stock data from Yahoo Finance and saves it in Parquet format.

    Args:
        tickers (list[str]): A list of stock tickers.
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.
        interval (str): The data interval (e.g., '1d' for daily, '1m' for minute).
    """
    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        if not data.empty:
            # Create directory structure
            output_dir = Path(f"data/processed/symbol={ticker}/interval={interval}")
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save data to Parquet file
            output_path = output_dir / "data.parquet"
            data.to_parquet(output_path)
            print(f"Data for {ticker} saved to {output_path}")
        else:
            print(f"No data found for {ticker}")

if __name__ == '__main__':
    # Example usage
    tickers_to_download = ["AAPL", "GOOG", "MSFT"]
    start = "2020-01-01"
    end = "2023-12-31"
    download_data(tickers_to_download, start, end)
