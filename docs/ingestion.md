# Data Ingestion

The `ingestion` module is responsible for downloading historical market data from various APIs and saving it in a standardized format.

## Data Sources

Currently, the only supported data source is **Yahoo Finance** (`yfinance`). However, the module is designed to be extensible, and new data sources can be added easily.

## Usage

The main entry point for the ingestion module is the `src/ingestion/yfinance_connector.py` script. You can run this script directly from the command line to download data for the tickers specified in the `TICKER_UNIVERSE` variable in `config.py`.

```bash
python src/ingestion/yfinance_connector.py
```

You can also use the interactive TUI to run the data ingestion process.

## Data Format

The downloaded data is saved in the `data/processed/` directory in **Parquet** format. The data is partitioned by `symbol` and `interval`. For example, the daily data for Apple (AAPL) would be stored in `data/processed/symbol=AAPL/interval=1D/data.parquet`.
