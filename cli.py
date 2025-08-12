
# Sovereign Local Quant (SLQ) TUI Dashboard
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.theme import Theme
from rich import box
import sys

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
    ("Research Idea", "Use SLM to research a new trading idea"),
    ("Run Backtest", "Run a backtest based on experiment config"),
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
        style = "option" if idx == selected else ""
        table.add_row(f"[{style}]{idx+1}. {option}[/{style}]", desc)
    console.print(table)

def ingest_data_screen():
    console.clear()
    show_banner()
    console.print("[highlight]Ingest Data[/highlight]\n")
    source = console.input("[menu]Enter data source (default: yfinance): [/menu]") or "yfinance"
    symbols = console.input("[menu]Enter symbols (comma-separated, default: SPY,QQQ): [/menu]") or "SPY,QQQ"
    console.print(f"[menu]Ingesting data from [highlight]{source}[/highlight] for symbols: [highlight]{symbols}[/highlight]...[/menu]")
    # TODO: Add actual ingestion logic here
    console.print("[success]Data ingestion complete![/success]")
    console.input("[menu]Press Enter to return to main menu...[/menu]")

def research_idea_screen():
    console.clear()
    show_banner()
    console.print("[highlight]Research Idea[/highlight]\n")
    idea = console.input("[menu]Describe your trading idea: [/menu]")
    console.print(f"[menu]Researching: [highlight]{idea}[/highlight]...[/menu]")
    # TODO: Add SLM orchestration logic here
    console.print("[success]Research complete![/success]")
    console.input("[menu]Press Enter to return to main menu...[/menu]")

def run_backtest_screen():
    console.clear()
    show_banner()
    console.print("[highlight]Run Backtest[/highlight]\n")
    config_path = console.input("[menu]Enter experiment config path (e.g., experiments/exp_20250812_LGBM_SPY_1D/config.json): [/menu]")
    console.print(f"[menu]Running backtest with config: [highlight]{config_path}[/highlight]...[/menu]")
    # TODO: Add backtesting logic here
    console.print("[success]Backtest complete![/success]")
    console.input("[menu]Press Enter to return to main menu...[/menu]")

def view_reports_screen():
    console.clear()
    show_banner()
    console.print("[highlight]View Reports[/highlight]\n")
    # TODO: List and display available reports
    console.print("[menu]No reports available yet. (Feature coming soon!)[/menu]")
    console.input("[menu]Press Enter to return to main menu...[/menu]")

def main_menu():
    selected = 0
    while True:
        console.clear()
        show_banner()
        show_menu(selected)
        try:
            choice = console.input("[menu]Select an option (1-5): [/menu]")
            if not choice.isdigit():
                raise ValueError
            choice = int(choice)
            if choice < 1 or choice > len(MENU_OPTIONS):
                raise ValueError
        except ValueError:
            console.print("[error]Invalid selection. Please enter a number between 1 and 5.[/error]")
            continue
        if choice == 1:
            ingest_data_screen()
        elif choice == 2:
            research_idea_screen()
        elif choice == 3:
            run_backtest_screen()
        elif choice == 4:
            view_reports_screen()
        elif choice == 5:
            console.print("[success]Exiting SLQ TUI. Goodbye![/success]")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
