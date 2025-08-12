# Sovereign Local Quant (SLQ) TUI Dashboard
import sys
from pathlib import Path
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.theme import Theme
from rich import box

from src.ingestion.downloader import download_data
from src.modeling.training import train_single_stock
from src.backtesting.engine import Backtester
from src.reporting.html_report import generate_html_report
from src.modeling.models.lightgbm_model import LightGBMModel

custom_theme = Theme({
    "banner_red": "bold red",
    "banner_blue": "bold blue",
    "banner_purple": "bold magenta",
    "menu": "bold cyan",
    "option": "bold yellow",
    "highlight": "bold magenta",
    "success": "bold green",
    "error": "bold red",
})

console = Console(theme=custom_theme)

ASCII_BANNER = """
[banner_red]███████╗[/banner_red][banner_blue]██╗     [/banner_blue][banner_purple] ██████╗ [/banner_purple][banner_red]    ███████╗[/banner_red]
[banner_red]██╔════╝[/banner_red][banner_blue]██║     [/banner_blue][banner_purple]██╔═══██╗[/banner_purple][banner_red]    ██╔════╝[/banner_red]
[banner_red]███████╗[/banner_red][banner_blue]██║     [/banner_blue][banner_purple]██║   ██║[/banner_purple][banner_red]    █████╗  [/banner_red]
[banner_red]╚════██║[/banner_red][banner_blue]██║     [/banner_blue][banner_purple]██║   ██║[/banner_purple][banner_red]    ██╔══╝  [/banner_red]
[banner_red]███████║[/banner_red][banner_blue]███████╗[/banner_blue][banner_purple]╚██████╔╝[/banner_purple][banner_red]    ██║     [/banner_red]
[banner_red]╚══════╝[/banner_red][banner_blue]╚══════╝[/banner_blue][banner_purple] ╚═════╝ [/banner_purple][banner_red]    ╚═╝     [/banner_red]
"""

MENU_OPTIONS = [
    ("Ingest Data", "Ingest market data from APIs"),
    ("Train and Backtest", "Train a model and run a backtest for a single stock"),
    ("View Reports", "View experiment and research reports"),
    ("Exit", "Exit the dashboard")
]

def show_banner():
    banner = Text.from_markup(ASCII_BANNER)
    console.print(Align.center(banner))
    console.print(Align.center("[banner_purple]Sovereign Local Quant (SLQ) Research Copilot[/banner_purple]"))
    console.print(Align.center("[menu]Decision Support TUI | Red, Blue, Purple Theme[/menu]\n"))

def show_menu(selected=0):
    table = Table(show_header=True, header_style="highlight", box=box.ROUNDED, expand=True)
    table.add_column("[menu]Option[/menu]", justify="center")
    table.add_column("[menu]Description[/menu]", justify="center")
    for idx, (option, desc) in enumerate(MENU_OPTIONS):
        if idx == selected:
            table.add_row(f"[option]{idx+1}. {option}[/option]", desc)
        else:
            table.add_row(f"{idx+1}. {option}", desc)
    console.print(table)

def ingest_data_screen():
    console.clear()
    show_banner()
    console.print("[highlight]Ingest Data[/highlight]\n")
    source = console.input("[menu]Enter data source (default: yfinance): [/menu]") or "yfinance"
    symbols_str = console.input("[menu]Enter symbols (comma-separated, default: SPY,QQQ): [/menu]") or "SPY,QQQ"
    symbols = [s.strip().upper() for s in symbols_str.split(',')]
    start_date = console.input("[menu]Enter start date (YYYY-MM-DD, default: 2020-01-01): [/menu]") or "2020-01-01"
    end_date = console.input("[menu]Enter end date (YYYY-MM-DD, default: 2023-12-31): [/menu]") or "2023-12-31"

    console.print(f"[menu]Ingesting data from [highlight]{source}[/highlight] for symbols: [highlight]{symbols}[/highlight]...[/menu]")

    try:
        download_data(symbols, start_date, end_date)
        console.print("[success]Data ingestion complete![/success]")
    except Exception as e:
        console.print(f"[error]An error occurred: {e}[/error]")

    console.input("[menu]Press Enter to return to main menu...[/menu]")

def train_and_backtest_screen():
    console.clear()
    show_banner()
    console.print("[highlight]Train and Backtest[/highlight]\n")
    ticker = console.input("[menu]Enter ticker symbol (e.g., AAPL): [/menu]").upper()

    if not ticker:
        console.print("[error]Ticker symbol cannot be empty.[/error]")
        console.input("[menu]Press Enter to return to main menu...[/menu]")
        return

    try:
        # Train the model
        train_single_stock(ticker)

        # Run backtest
        model_path = f"experiments/{ticker}_model.pkl"
        data_path = f"data/processed/symbol={ticker}/interval=1d/data.parquet"

        model = LightGBMModel()
        model.load(model_path)

        df = pd.read_parquet(data_path)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        backtester = Backtester(model.model, df)
        results = backtester.run()

        # Generate report
        report_path = f"experiments/{ticker}_report.html"
        generate_html_report(results, ticker, report_path)

        console.print("[success]Training, backtesting, and reporting complete![/success]")
        console.print(f"View the report at: [highlight]{report_path}[/highlight]")

    except Exception as e:
        console.print(f"[error]An error occurred: {e}[/error]")

    console.input("[menu]Press Enter to return to main menu...[/menu]")

def view_reports_screen():
    console.clear()
    show_banner()
    console.print("[highlight]View Reports[/highlight]\n")

    reports = list(Path("experiments").glob("*_report.html"))

    if not reports:
        console.print("[menu]No reports available yet.[/menu]")
    else:
        table = Table(show_header=True, header_style="highlight", box=box.ROUNDED)
        table.add_column("Report File", justify="left")
        for report in reports:
            table.add_row(str(report))
        console.print(table)

    console.input("[menu]Press Enter to return to main menu...[/menu]")

def main_menu():
    selected = 0
    while True:
        console.clear()
        show_banner()
        show_menu(selected)
        try:
            choice_str = console.input("[menu]Select an option (1-4): [/menu]")
            if not choice_str.isdigit():
                raise ValueError
            choice = int(choice_str)
            if choice < 1 or choice > len(MENU_OPTIONS):
                raise ValueError
        except (ValueError, KeyboardInterrupt):
            console.print("[error]Invalid selection. Please enter a number between 1 and 4.[/error]")
            continue

        if choice == 1:
            ingest_data_screen()
        elif choice == 2:
            train_and_backtest_screen()
        elif choice == 3:
            view_reports_screen()
        elif choice == 4:
            console.print("[success]Exiting SLQ TUI. Goodbye![/success]")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
