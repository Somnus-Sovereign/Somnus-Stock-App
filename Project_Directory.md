# Project Directory: SLM in Local Quant Stack

This document serves as the central tracker and living blueprint for the Sovereign Local Quant (SLQ) project. It expands upon the initial `base_idea.md` to provide a detailed guide for development, architecture, and future milestones.

---

## 1. Core Principles & Philosophy

This project is a **decision-support copilot**, not an automated trading bot. Its primary goal is to augment human research with systematic, reproducible analysis in a secure, private, and cost-effective environment.

* **Sovereign & Local-First:** All data, models, and code reside locally. No reliance on external cloud services for core processing. This ensures privacy, control, and zero operational cost.
* **Human-in-the-Loop:** The system generates signals, reports, and backtests. A human makes the final decision to execute any trade, respecting brokerage terms of service and regulatory guidelines.
* **Reproducibility is Paramount:** Every output must be traceable. Actions taken by the SLM or other components must log the exact code, data hashes, and seeds used to generate the result.
* **Security by Design:** API keys and secrets are managed via `.env` files and are never to be included in prompts, logs, or source code. Data scraping is restricted to public sources.

---

## 2. System Architecture

The architecture is designed to be a modular, unidirectional pipeline from raw data to human-gated execution.

```diagram
┌──────────┐        ┌───────────────┐        ┌─────────────┐        ┌────────────┐
│ Data APIs│  --->  │ Ingest/Schema │  --->  │ Feature Lab │  --->  │  Models    │
│  (prices,│        │  Normalizer   │        │  (SLM helps)│        │  (TS/ML)   │
│ news, fx)│        └───────┬───────┘        └──────┬──────┘        └─────┬──────┘
└─────┬────┘                │                     Experiments             │
      │                  DuckDB/Parquet            (walk-forward)         │
      ▼                     │                       ▼                     ▼
┌───────────┐               ▼                                         ┌───────────┐
│ Secrets   │          ┌────────────┐            ┌────────────┐       │ Risk/PM   │
│ (.env)    │          │ Backtester │ <———logs—— │ SLM Reports│       │ (sizing/  │
└─────┬─────┘          └────┬───────┘            └────────────┘       │ limits)   │
      │                     │                                         └────┬──────┘
      ▼                     ▼                                              ▼
                     ┌──────────────┐                                 ┌────────────┐
                     │  Dash/TUI    │  <—— human approves trades ——>  │ Brokerage  │
                     └──────────────┘                                 │  (manual)  │
                                                                      └────────────┘
```

---

## 3. Directory & File Manifest

This structure organizes the project for clarity, modularity, and deterministic execution.

```directory_tree
Somnus_Stock_App/
├── .gitignore
├── Project_Directory.md
├── README.md
├── cli.py
├── config.py
├── data/
│   ├── processed/
│   └── raw/
├── experiments/
│   └── exp_20250812_LGBM_SPY_1D/
│       ├── config.json
│       ├── model.pkl
│       ├── report.html
│       └── run_log.txt
├── notebooks/
├── requirements.txt
├── secrets/
│   ├── .env
│   └── .env.example
├── setup.sh
├── src/
│   ├── backtesting/
│   ├── features/
│   │   ├── generated/
│   │   └── library/
│   ├── ingestion/
│   ├── modeling/
│   │   ├── models/
│   │   └── training.py
│   ├── reporting/
│   └── slm/
│       ├── orchestrator.py
│       └── tools.py
└── tests/
    ├── test_backtester.py
    └── test_features.py
```

### File Descriptions

* `README.md`: High-level project overview and setup instructions for new users.
* `Project_Directory.md`: **(This file)** The living blueprint and central tracker.
* `requirements.txt`: A list of all Python dependencies for `pip install -r requirements.txt`.
* `setup.sh`: A simple shell script to create a virtual environment and install dependencies.
* `cli.py`: The main entry point for the application. Provides a full-featured interactive TUI dashboard using the `rich` library, with a red, blue, and purple color scheme and an ASCII art banner. The TUI allows users to navigate, run research, view reports, and manage experiments in a user-friendly interface. All commands and workflows are accessible via the TUI.
* `config.py`: A Python-based configuration module. Replaces YAML with dynamic, code-based settings for things like data sources, model parameters, and backtest settings.
* `.gitignore`: Standard Python gitignore to exclude `__pycache__`, `.venv`, `.env`, etc.
* `data/`: **Lakehouse Root**
  * `raw/`: Raw, immutable data from APIs (e.g., JSON, CSV).
  * `processed/`: Cleaned, normalized, and partitioned Parquet files (e.g., `symbol=AAPL/interval=1D/data.parquet`).
* `secrets/`:
  * `.env`: Holds API keys and other secrets. **This file is never committed to version control.**
  * `.env.example`: A template showing what variables are needed.
* `src/`: **Core Logic**
  * `ingestion/`: Modules for pulling data from various APIs (e.g., `alpha_vantage.py`, `yfinance.py`).
  * `features/library/`: Core feature generation functions (e.g., TA-lib, rolling stats).
  * `features/generated/`: SLM-generated feature modules. These are checked into version control.
  * `modeling/models/`: Implementations of forecasting models (e.g., `lightgbm_model.py`, `nbeats_model.py`).
  * `modeling/training.py`: Logic for training, validation, and saving models.
  * `backtesting/`: The walk-forward backtesting engine, including risk and portfolio management logic.
  * `reporting/`: Modules for generating reports (e.g., P&L curves, metrics tables).
  * `slm/tools.py`: The defined "tool-use DSL" the SLM can call (e.g., `run_backtest(...)`, `generate_features(...)`).
  * `slm/orchestrator.py`: The main logic for interacting with the GGUF model.
* `experiments/`: Each subdirectory contains a single experiment run, including config, model, report, and logs.
* `notebooks/`: Jupyter notebooks for exploratory data analysis (EDA) and ad-hoc research.
* `tests/`: Unit tests for critical components like feature generation and the backtester.

---

## 4. Development Roadmap & Milestones

### Milestone 1: Minimum Viable Product (The "Weekend Build")

**Goal:** Prove the core concept by building a simple end-to-end pipeline.

1. **[ ] Ingestion:**
    * Implement a data connector for a single source (e.g., `yfinance`).
    * Write a script to pull 1-minute and daily bars for a small universe of equities (e.g., SPY, QQQ).
    * Store data in the `data/processed/` directory as Parquet files.
2. **[ ] Feature Generation:**
    * Create a basic feature library in `src/features/library/` with functions for: returns, volatility, RSI, rolling skew, and day-of-week.
3. **[ ] Modeling:**
    * Implement a LightGBM classification model (`up`/`down` for the next day).
    * Create a training script that uses a simple walk-forward validation split (e.g., 3 years train, 6 months test).
4. **[ ] Backtesting:**
    * Build a basic backtester that accounts for simple fees and slippage.
    * Implement a simple strategy (e.g., long top N signals, beta-neutral).
5. **[ ] Reporting:**
    * Generate an HTML report with an equity curve, key performance metrics (Sharpe, Drawdown), and feature importances.
6. **[ ] Human Gate:**
    * Create a full-featured TUI dashboard (using `rich`) that shows proposed trades, experiment results, and allows interactive navigation. The TUI features a red, blue, and purple color scheme and an ASCII art banner for branding.

### Milestone 2: SLM Integration & Feature Lab

**Goal:** Integrate the SLM to automate feature engineering and experiment generation.

1. **[ ] SLM Orchestrator:**
    * Set up the GGUF model runner in `src/slm/orchestrator.py`.
    * Define the tool-use DSL in `src/slm/tools.py`.
2. **[ ] Feature Generation Tool:**
    * Create a tool `generate_features(specs: dict)` that the SLM can call. The SLM will provide a dictionary of feature specifications, and the tool will write the corresponding Python code to `src/features/generated/`.
3. **[ ] Experiment Tool:**
    * Create a tool `run_experiment(config: dict)` that the SLM can call to trigger a full backtest run based on a configuration it generates.
4. **[ ] CLI Integration:**
    * Add a new CLI command: `python cli.py research "I want to test if RSI combined with volume spikes predicts returns on tech stocks."`

### Milestone 3: Advanced Modeling & Scenario Analysis

**Goal:** Expand the modeling stack and implement the "Future Mappings" concept.

1. **[ ] Advanced Models:**
    * Integrate N-BEATS or a Temporal Fusion Transformer (TFT) for time-series forecasting.
    * Implement a Hidden Markov Model (HMM) for regime detection.
2. **[ ] Scenario Engine:**
    * Build the Monte Carlo simulation engine that consumes the JSON/dict-based scenario definitions.
3. **[ ] SLM Scenario Generation:**
    * Fine-tune the SLM prompt to translate natural language narratives (e.g., "hawkish Fed") into structured shock vectors for the simulation engine.

---

## 5. Setup & Usage

1. **Initial Setup:**

    ```bash
    # Clone the repository (if applicable)
    # cd trents_stock_app

    # Run the setup script to create a virtual environment and install packages
    bash setup.sh  # or use setup.ps1 on Windows

    # Activate the environment
    source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows

    # Copy the example secrets file and add your API keys
    cp secrets/.env.example secrets/.env
    # Edit .env with your favorite editor
    ```

2. **Running Commands:**

    ```bash
    # Launch the interactive TUI dashboard
    python cli.py

    # All features (ingest, backtest, research, reports) are accessible via the TUI menu.
    ```

## 6. Technical Stack & Dependencies

| Layer | Technology | Reasoning |
|-------|------------|-----------|
| **Language** | Python 3.11 | Modern typing, async support, rich ecosystem for data science. |
| **Data Storage** | Parquet + DuckDB | Columnar format for fast analytics; DuckDB provides SQL on local files without a server. |
| **ML Frameworks** | LightGBM, PyTorch (N-BEATS), Optuna | Gradient-boosted trees for tabular, deep nets for sequence forecasting, hyper-parameter search. |
| **Feature Engineering** | NumPy, pandas, TA-Lib (optional) | Vectorised ops, rolling windows, technical indicators. |
| **LLM Integration** | GGUF model run via `llama.cpp` (or `ctransformers`) | Offline, GPU-accelerated inference; no external API calls. |
| **CLI/TUI** | Rich, Textual | Full-screen terminal UI with colour scheme and ASCII banner. |
| **Reporting** | Jinja2, Plotly, Pandas-Styling | Interactive HTML reports, exportable CSV/JSON. |
| **Testing** | pytest, hypothesis | Unit, property-based, and integration tests. |
| **CI/CD** | GitHub Actions, Black, Flake8, MyPy | Automated linting, type-checking, testing, and artifact publishing. |
| **Security** | python-dotenv, bb7_security_audit, sandboxed execution (`bb7_python_execute_secure`) | Secrets isolation, static analysis, runtime sandbox. |

## 7. Detailed Directory & File Responsibilities

```file_tree
src/
├── ingestion/
│   ├── __init__.py                # expose public ingest API
│   ├── yfinance.py                # wrapper around yfinance, returns raw OHLCV + fundamentals
│   ├── alpha_vantage.py           # generic REST client with rate-limit handling
│   └── loader.py                  # orchestrates parallel downloads, validates schemas, writes to data/raw/
├── features/
│   ├── library/                   # hand-crafted deterministic feature functions
│   │   ├── returns.py
│   │   ├── volatility.py
│   │   └── technical_indicators.py
│   └── generated/                 # SLM-generated modules, version-controlled
│       └── <auto_*.py>
├── modeling/
│   ├── models/
│   │   ├── base_model.py          # abstract BaseModel with fit/predict/save/load
│   │   ├── lightgbm_model.py
│   │   └── nbeats_model.py
│   └── training.py                # walk-forward split, hyper-opt integration
├── backtesting/
│   ├── engine.py                  # core walk-forward backtester
│   ├── risk.py                    # position sizing, drawdown caps, transaction cost model
│   └── utils.py                   # trade-log helpers, metrics calculators
├── reporting/
│   ├── html_report.py             # Jinja2 template renderer
│   └── metrics.py                 # Sharpe, Sortino, Calmar, turnover calculations
├── slm/
│   ├── orchestrator.py            # loads GGUF model, maintains session state
│   └── tools.py                   # tool-use DSL (run_backtest, generate_features, etc.)
└── utils/
    ├── logger.py                  # structured JSON logging, audit trail
    └── config_loader.py           # loads config.py and validates schema
```

*Each module includes comprehensive docstrings and type hints to aid IDE assistance and static analysis.*

## 8. Expanded Development Roadmap

### Milestone 1 – Minimum Viable Product (Weekend Build)

* **Ingestion** – `yfinance` connector, raw → Parquet pipeline, SHA-256 manifest.
* **Feature Lab** – 10 core deterministic features, unit-tested.
* **Modeling** – LightGBM binary classifier, walk-forward validation (3 y train / 6 m test).
* **Backtesting** – Simple fee model, equity-curve logging, CSV trade log.
* **Reporting** – HTML report with Plotly equity curve, feature importance heatmap.
* **TUI** – Rich dashboard with colour scheme, ASCII banner, navigation to all stages.

### Milestone 2 – SLM Integration & Feature Lab Automation

* **Orchestrator** – GGUF model wrapper, persistent session, tool-dispatch.
* **Tool: `generate_features`** – Accepts JSON spec, writes deterministic Python module to `src/features/generated/`.
* **Tool: `run_experiment`** – Takes experiment config, triggers full pipeline, stores results under `experiments/`.
* **CLI Extension** – `cli.py research "<natural language query>"` routes to SLM.

### Milestone 3 – Advanced Modeling & Scenario Analysis

* **Models** – Add N-BEATS (forecasting) and HMM (regime detection).
* **Scenario Engine** – Monte-Carlo shock generator consuming SLM-produced JSON vectors.
* **SLM Prompt Library** – Templates for macro narratives → structured shock definitions.

### Milestone 4 – Production-Ready Enhancements

* **Dockerisation** – Optional container for reproducible environments.
* **Versioned Lakehouse** – Time-travel queries via DuckDB snapshots.
* **Automated Hyper-Opt** – Optuna study orchestration across GPU/CPU resources.
* **Compliance Dashboard** – Exportable audit logs, GDPR-friendly data handling.

## 9. Testing Strategy

| Scope | Tool | Key Assertions |
|-------|------|----------------|
| Unit | `pytest` | 90% coverage on feature functions, model wrappers. |
| Property-Based | `hypothesis` | Invariants on data shapes, NaN-free pipelines. |
| Integration | `pytest` + temporary DuckDB | End-to-end ingestion → feature → model → backtest. |
| UI | `rich.console` capture | TUI renders without exceptions, colour scheme applied. |
| SLM Tools | Custom harness using `bb7_python_execute_secure` | Tool contracts (input validation, deterministic output). |
| Security | `bb7_security_audit` | No unsafe imports, no exec of user-provided code. |

All tests run on every push via GitHub Actions; failures block merges.

## 10. CI/CD Pipeline

`.github/workflows/ci.yml` (summary):

1. **Setup** – Python 3.11, cache pip, install `requirements.txt`.
2. **Lint** – `black --check .`, `flake8`, `mypy --strict`.
3. **Security** – `bb7_security_audit` on all `src/` files.
4. **Test** – `pytest --cov=src`.
5. **Build** – `python -m build` → wheel & sdist.
6. **Publish** – On tag, upload artifacts to GitHub Packages (private PyPI).

Release script (`release.sh`) automates version bump, changelog generation, git tag, and wheel upload.

## 11. Security & Compliance

* **Secrets** – Loaded via `python-dotenv`; never logged (`bb7_memory_store` with `category="secret"`).
* **Audit Trail** – Every SLM tool call logs a `ToolResult` JSON line (`logs/tool_audit.log`) with hash of inputs/outputs.
* **Sandboxed Execution** – All generated code runs through `bb7_python_execute_secure` (resource limits, no network).
* **Data Privacy** – Only public market data stored; no PII. Retention policies enforced via `data/metadata.json`.
* **Static Analysis** – `bb7_security_audit` + `bb7_analyze_code_complete` on PRs.

## 12. Future Enhancements & Concepts

* **Meta-Learning** – Use SLM to propose hyper-parameter priors based on past experiments.
* **Explainable AI** – SHAP integration for model interpretability, auto-generated narrative explanations.
* **Live-Data Bridge** – Optional websocket connector for low-latency price feeds (still human-gated).
* **Plugin Architecture** – Register new ingestion providers or model families via a `plugins/` entry-point.
* **Knowledge Graph** – Persist concepts extracted by `bb7_memory_extract_concepts` to power semantic search across experiments.

## 13. Glossary

| Term | Definition |
|------|------------|
| **SLM** | Sovereign Local Model – the offline GGUF LLM acting as a research copilot. |
| **Lakehouse** | Unified storage layer (Parquet + DuckDB) enabling both file-based and SQL analytics. |
| **Walk-forward** | Sequential out-of-sample validation that mimics live trading. |
| **Feature Lab** | Ecosystem of deterministic hand-crafted and SLM-generated feature modules. |
| **Human-Gate** | Manual approval step before any trade execution. |
| **Tool-Use DSL** | Structured JSON commands the SLM can invoke to run code, backtests, or generate features. |
| **Audit Log** | Immutable JSON record of every tool invocation, data hash, and code version. |

## 14. References & Further Reading

* Chan, Ernest P. *Algorithmic Trading* (2nd ed.) – quantitative strategy fundamentals.  
* Hyndman & Athanasopoulos, *Forecasting: Principles and Practice* – time-series modeling.  
* OpenAI Cookbook – “Best practices for tool-use”.  
* DuckDB Docs – <https://duckdb.org/docs/>  
* LightGBM Docs – <https://lightgbm.readthedocs.io/>  
* N-BEATS Paper – Oreshkin et al., “N-BEATS: Neural Basis Expansion Analysis for Interpretable Time Series Forecasting”.  

---  

*All modifications are logged via `bb7_log_event(event_type="doc_update", description="Expanded Project_Directory.md", details={"sections_added":13})` to maintain traceability.*
