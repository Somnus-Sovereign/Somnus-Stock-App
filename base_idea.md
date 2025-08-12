# **SLM in Local Quant Stack**

## 1) Purpose & safety rails (read-first)

* **Decision support, not auto-trading.** Keep it as a research/copilot that proposes signals and backtests. You (or your brother) click “execute” manually to avoid brokerage TOS/regulatory snags.
* **No non-public info, no scrapes behind auth walls, no data sharing.** Keep API keys in `.env`, never in prompts, never in logs.
* **Reproducibility beats vibes.** Every SLM action should emit the exact SQL/Python it ran and a manifest of inputs → outputs.

## 2) System sketch (sovereign & modular)

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
                     │   TUI Dash   │  <—— human approves trades ——>  │ Brokerage  │
                     └──────────────┘                                 │  (manual)  │
                                                                      └────────────┘
```

## 3) What the SLM should do (and not do)

**Do (great fits for a 1–7B GGUF model):**

* Pull data via API keys, map schemas, generate **DuckDB** tables, dedupe, resample to regimes (1m/5m/1h/daily).
* Generate **feature code** on request: TA-Lib indicators, rolling stats, realized vol, gaps, session features, event flags (earnings, FOMC days).
* Create **experiment manifests**: “train XGBoost on features A..Z with walk-forward CV, horizon=1d, include slippage=6 bps, fees=2 bps.”
* Draft **risk reports**: P\&L curve, Sharpe/Sortino, max DD, turnover, exposure by sector/factor.

**Avoid:**

* “LLM predicts tomorrow’s price is 1.23.” LLMs hallucinate; use proper TS/ML for forecasts.

## 4) Modeling stack (deterministic core)

* **Forecasting/Classification:**

  * Tabular: **LightGBM/XGBoost**, logistic for up/down, regression for expected return.
  * Time series: **ARIMA/TBATS** for baselines; **N-BEATS / TFT (Temporal Fusion Transformer)** for richer patterns; **DeepAR** for multi-series.
* **Regime detection:** Hidden Markov Models, spectral clustering on returns/vol; or simple rolling z-scores of vol/skew.
* **Ensembles:** Stack a linear model + gradient boosting + simple TS model; average by out-of-sample performance.
* **Backtesting:** **Walk-forward** with realistic constraints: slippage, fees, borrow costs, delay, position limits, risk caps.

**Metrics:** Sharpe, Sortino, max drawdown, Calmar, hit rate, average win/loss, turnover, exposure concentration, **probability of ruin**.

## 5) “Future mappings” (turn narratives into scenarios)

Use the SLM to **codify scenarios**, then simulate with orthodox math:

* **Macro → shock vectors:** Translate “hawkish Fed + energy spike” into delta paths on rates/oil, then run **VAR/SVAR** to propagate into sector returns.
* **Regime trees:** SLM writes a YAML/JSON-free schema (since you deprecate YAML) like:

  ```json
  {
    "scenario": "EnergyShock",
    "shocks": {
      "oil": "+15%",
      "usd": "+2%",
      "yield10y": "+40bp"
    },
    "map_to": {
      "factors": ["value↑", "momentum↓", "smallcaps↓"]
    },
    "horizon": "20d",
    "n": 5000,
    "corr": {
      "type": "copula",
      "params": {
        "distribution": "student_t",
        "df": 6
      }
    }
  }

```yaml
{
    "scenario": "EnergyShock",
    "shocks": {
      "oil": "+15%",
      "usd": "+2%",
      "yield10y": "+40bp"
    },
    "map_to": {
      "factors": ["value↑", "momentum↓", "smallcaps↓"]
    },
    "horizon": "20d",
    "n": 5000,
    "corr": {
      "type": "copula",
      "params": {
        "distribution": "student_t",
        "df": 6
      }
    }
}
```

The engine consumes this and runs **Monte Carlo** over the portfolio.

## 6) Data & features (high signal, low leakage)

* **Price/volume**: OHLCV, VWAP, rolling mean/vol/skew/kurtosis; ATR; gap/overnight returns.
* **Microstructure**: if you have L2/quotes—imbalance, order-book slope, queue length (downsampled).
* **Calendar/events**: earnings days, options expiry, FOMC, CPI; session opens/close proximity.
* **Cross-asset**: sector ETFs, rates, credit, DXY, WTI/Brent, gold; PCA factors.
* **Text** (optional, still sovereign): local PDF/HTML of filings/PRs → embed to vectors; SLM does **entity/metric extraction** (not sentiment hand-waving) and emits discrete features: “guidance\_raised=1”, “buyback\_announced=1”.

## 7) Storage & plumbing (local-first)

* **DuckDB + Parquet** as the lakehouse; cheap, fast, no server.

* **Project structure** (no YAML; use your Bayesian/dynamic config idea):

```file_tree
  /data/            # parquet partitions by symbol/interval
  /secrets/         # .env (never prompt-exposed)
  /features/        # SLM-generated .py feature modules (checked in)
  /models/          # saved weights + config manifests (JSON)
  /experiments/     # auto-named runs with seeds + reports
  /reports/         # human-readable HTML/MD + charts
  /cli.py           # Launches the interactive TUI dashboard

directory

```

* **Determinism:** Every run stamped with **seed**, data snapshot hash, exact code refs. SLM must print the code it wrote.

## 8) Risk & portfolio layer

* **Sizing:** volatility targeting; capped Kelly (e.g., 0.2–0.5×); risk parity across signals.
* **Constraints:** position caps per name/sector; hard stop on drawdown (daily/rolling).
* **Execution realism:** bar-close or next-bar open; no look-ahead; latency buffer.
* **Kill-switch:** if live slippage > X bps or drift from model > Y std, drop to cash.

## 9) Suggested SLMs (local, tiny → mid)

Any **1–7B instruct** model in **GGUF** works for orchestration/text-to-code (quantized Q4–Q5). You don’t need 13B+ for this role. Keep a **tool-use DSL** that the SLM calls (e.g., `make_features([...])`, `backtest(cfg)`) instead of letting it freestyle the whole pipeline.

## 10) Minimal flow to prove it works (weekend build)

1. **Ingest**: one equities universe, 1m and daily bars → DuckDB.
2. **Features**: returns, vol, RSI, rolling skew, gap, day-of-week, earnings flag.
3. **Model**: LightGBM classification (up/down next day), walk-forward 3y→6m steps.
4. **Backtest**: fees/slippage on; top-N long (or long/short with beta-neutral cap).
5. **Report**: HTML with equity curve, table of metrics, confusion matrix, feature importances.
6. **Human gate**: TUI dashboard proposes trades, displays experiment results, and allows interactive navigation. The TUI features a red, blue, and purple color scheme and an ASCII art banner for branding. All user interaction is through this TUI.

## 11) Compliance footnotes (not legal advice)

* Personal trading is generally fine; once you start managing others’ money or distributing signals, rules change fast.
* Many brokers disallow unattended bots; **keep a human-in-the-loop** and review TOS.
* Log everything; keep it audit-ready.