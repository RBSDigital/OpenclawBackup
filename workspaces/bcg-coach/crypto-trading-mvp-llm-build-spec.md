# Crypto Trading Research MVP

## LLM build specification

**Status:** Approved implementation brief  
**Version:** 1.0  
**Date:** 16 October 2026  
**Primary audience:** An LLM or engineering agent responsible for building the project  
**Source:** Derived from the reviewed Crypto Trading MVP BRD v1.2

## 1. Build objective

Build a manual, research-only Python application that an operator can run each morning to:

1. select one cryptocurrency or a configured asset universe;
2. retrieve historical and current spot-market data;
3. validate and persist the data with full provenance;
4. run a controlled set of candidate trading strategies;
5. backtest each strategy using realistic fees, spread, slippage and execution timing;
6. reject strategies that fail data, risk, robustness or out-of-sample gates; and
7. produce a reproducible report and machine-readable result bundle.

The first release is an MVP for research and decision support. It must not place orders, manage funds or claim that historical performance predicts future returns.

## 2. Non-negotiable boundaries

### In scope

- Spot markets only.
- Kraken Spot as the first exchange and execution-venue data source.
- Public market-data access only.
- CCXT as the initial exchange abstraction, with a direct Kraken adapter available where CCXT loses important detail.
- Daily and hourly OHLCV bars initially.
- Python managed with `uv` and a committed `uv.lock` file.
- Parquet for immutable raw and curated datasets.
- DuckDB for local analytical queries.
- VectorBT for vectorised research and portfolio simulation.
- A CLI that works without n8n.
- Optional n8n orchestration for triggers, status, notifications and bounded retries.
- Tests, provenance, data-quality checks and reproducible reports.

### Explicitly out of scope

- Live order placement or automated execution.
- Private exchange credentials in the MVP.
- Custody, deposits, withdrawals or wallet management.
- Leverage, margin, futures, perpetuals, options or borrowing.
- High-frequency or latency-sensitive trading.
- Machine-learning price prediction as a first release.
- Tax calculation, investment advice or guaranteed profitability.
- n8n as the backtesting engine or source of strategy logic.
- A public web application or multi-user account system.

## 3. Core design decision

Use the following separation of responsibilities:

```text
n8n or manual CLI trigger
        |
        v
Python configuration and research pipeline
        |
        +--> market-data retrieval and provenance
        +--> validation and normalisation
        +--> Parquet/DuckDB storage
        +--> strategy execution
        +--> backtesting and cost model
        +--> risk and robustness gates
        +--> report and result bundle
        |
        v
Optional n8n status update and notification
```

Python is the authoritative execution path. The project must run successfully if n8n is stopped, unavailable or removed. n8n is a control-plane convenience, not a quantitative dependency.

The technically simplest baseline is a CLI plus cron/systemd timer. Add n8n after the CLI workflow is stable because the operator already knows n8n and may benefit from visual workflow control and notifications.

## 4. Recommended technology stack

### Required

- Python 3.12 or a later version confirmed compatible with the selected libraries.
- `uv` for project creation, dependency management, locking and execution.
- CCXT for the initial exchange adapter.
- `pandas` and NumPy at the strategy boundary.
- VectorBT for parameterised research and backtesting.
- PyArrow for Parquet I/O.
- DuckDB for local analysis.
- Pydantic or equivalent typed configuration validation.
- pytest for automated testing.
- A structured logging library or Python logging with JSON output.

### Optional or later

- Polars only if profiling shows that ingestion or transformation is a bottleneck.
- Direct Kraken REST/WebSocket calls where CCXT does not expose required semantics.
- CoinGecko for asset discovery and cross-source checks, never as an unlabelled substitute for Kraken execution-venue prices.
- Docker for repeatable deployment.
- n8n self-hosted with Docker Compose for orchestration after the manual pipeline is proven.
- Rust only after profiling demonstrates a material performance bottleneck that Python, VectorBT and data layout cannot address.

## 5. Project structure

Create this repository structure:

```text
crypto-trading-mvp/
├── pyproject.toml
├── uv.lock
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── src/crypto_trading/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── models.py
│   ├── logging_config.py
│   ├── venues/
│   │   ├── __init__.py
│   │   ├── protocol.py
│   │   ├── ccxt_kraken.py
│   │   └── native_kraken.py
│   ├── data/
│   │   ├── fetch.py
│   │   ├── validate.py
│   │   ├── normalise.py
│   │   ├── provenance.py
│   │   └── store.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── protocol.py
│   │   ├── baselines.py
│   │   ├── trend.py
│   │   ├── momentum.py
│   │   ├── mean_reversion.py
│   │   └── registry.py
│   ├── backtest/
│   │   ├── costs.py
│   │   ├── execution.py
│   │   ├── splits.py
│   │   ├── runner.py
│   │   ├── metrics.py
│   │   └── gates.py
│   └── reporting/
│       ├── report.py
│       ├── schemas.py
│       └── templates/
├── configs/
│   ├── example.toml
│   └── strategies.toml
├── data/                 # local or mounted; ignored by Git
├── reports/              # generated artefacts; policy-defined retention
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── n8n/
│   ├── workflows/
│   ├── README.md
│   └── docker-compose.example.yml
└── docs/
    ├── methodology.md
    ├── data-dictionary.md
    └── operations-runbook.md
```

## 6. Configuration contract

Use a validated TOML or YAML configuration. The implementation may choose one format, but the configuration must be versionable, human-readable and hashable.

Minimum fields:

```toml
run_name = "daily-research"
venue = "kraken"
symbol = "BTC/USD"
timeframe = "1h"
lookback_days = 730
timezone = "UTC"
data_dir = "data"
report_dir = "reports"
dry_run = true

[screening]
enabled = false
symbols = ["BTC/USD", "ETH/USD"]

[costs]
fee_bps = 40
spread_bps = 10
slippage_bps = 10
execution = "next_bar_open"

[gates]
minimum_observations = 500
maximum_drawdown = 0.35
minimum_trade_count = 10
require_non_negative_oos_net_return = true
require_no_data_quality_blocker = true
```

Do not present these values as proven thresholds. They are configuration examples and must be confirmed during calibration. Every run must record the exact configuration and its hash.

## 7. Data model and provenance

### Canonical OHLCV fields

At minimum, store:

- `timestamp_utc`
- `venue`
- `native_symbol`
- `canonical_symbol`
- `timeframe`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `is_complete_bar`
- `source_run_id`

Use UTC internally. Retain the original exchange timestamp and document candle-boundary semantics.

### Run manifest

Each run must create a manifest containing:

- `run_id`
- start and end timestamps in UTC;
- source code version or Git commit;
- dependency lock hash;
- configuration hash;
- provider and venue;
- symbols and timeframes;
- endpoint or adapter version;
- raw-data artefact paths and checksums;
- validation results;
- strategy versions and parameters;
- cost assumptions;
- result artefact paths;
- final status: `pass`, `fail`, `inconclusive` or `data_quality_blocked`.

Never silently overwrite raw data. Corrections create a new versioned artefact.

## 8. Manual morning workflow

Implement this sequence as a single documented CLI command, for example:

```bash
uv run crypto-research run --config configs/example.toml
```

The command must:

1. Load and validate configuration.
2. Generate a run ID.
3. Discover and validate the requested market and symbol.
4. Fetch public Kraken data through the exchange adapter.
5. Persist the raw response or a lossless raw equivalent with metadata.
6. Validate timestamps, gaps, duplicates, ordering, impossible prices, zero or negative values, stale bars and incomplete latest bars.
7. Normalise the data into the canonical schema.
8. Write curated Parquet and make it queryable through DuckDB.
9. Run buy-and-hold and no-trade baselines.
10. Run registered strategies with the active cost model.
11. Apply chronological train, validation and out-of-sample splits.
12. Run sensitivity and robustness tests.
13. Apply rejection gates.
14. Generate Markdown or HTML and JSON or Parquet results.
15. Write the manifest and exit with a meaningful status code.

“No strategy passed” is a successful research outcome, not a system error.

## 9. Initial strategy library

Implement strategies behind a common protocol. Each strategy must accept canonical market data and validated parameters and return venue-neutral signals. It must not import exchange-specific code.

Initial strategies:

1. Buy-and-hold baseline.
2. No-trade baseline.
3. Moving-average trend strategy.
4. Breakout or momentum strategy.
5. Mean-reversion strategy.
6. Configurable volatility or position-sizing rule.

Each strategy requires:

- a stable name and version;
- parameter schema and defaults;
- plain-English description;
- preconditions and minimum data requirements;
- unit tests;
- a deterministic result for a fixed dataset and configuration;
- explicit signal timing;
- documented limitations.

Do not add machine learning, sentiment or complex ensembles until the baseline methodology is demonstrably sound.

## 10. Backtesting rules

The engine must enforce the following:

- Signals at time `t` may use only information available before the simulated fill.
- Time-series observations must never be randomly shuffled.
- Parameter selection must not use the final out-of-sample period.
- Use chronological train, validation and test periods or walk-forward evaluation.
- Model venue fees, spread, slippage and execution timing.
- Define whether fills occur at the next open, next available price, close or another explicitly simulated convention.
- Apply liquidity limits and reject insufficiently liquid assets where required.
- Record the number of strategies and parameter combinations tested.
- Compare all strategies with baselines on equivalent periods and assumptions.
- Treat missing or suspect data as a warning or block, never silently interpolate.

Required reported metrics:

- gross return and net return;
- annualised or period-normalised return where appropriate;
- volatility;
- maximum drawdown;
- risk-adjusted return metric with definition;
- trade count;
- turnover;
- win rate;
- average win and loss;
- exposure and time in market;
- performance by train, validation and out-of-sample period;
- sensitivity to costs and key parameters.

## 11. Rejection gates

Make gates configurable and visible in the report. A strategy must be rejected or marked inconclusive when any applicable gate fails:

- insufficient observations;
- unresolved data-quality blocker;
- leakage or look-ahead warning;
- negative net out-of-sample performance when non-negative performance is required;
- excessive drawdown;
- insufficient trade count for interpretation;
- materially unstable neighbouring parameters;
- failure under adverse fee or slippage assumptions;
- unexplained difference between raw and curated data.

The system must not select the highest historical return automatically.

## 12. n8n integration contract

n8n is optional. The Python CLI must be the canonical interface.

### Allowed n8n responsibilities

- Manual trigger.
- Scheduled trigger.
- Passing a validated configuration reference.
- Invoking the Python CLI or a Python container.
- Capturing run ID, exit code, status and timestamps.
- Sending success, failure and data-quality notifications.
- Linking to the generated report and result bundle.
- Applying bounded retries around a failed invocation.

### Prohibited n8n responsibilities

- Reimplementing strategy logic.
- Performing numerical backtests in workflow nodes.
- Storing the canonical configuration as an unversioned workflow field.
- Requiring n8n for a manual recovery run.
- Storing exchange credentials in the research-only MVP.

### n8n controls

- Use a pinned workflow export under `n8n/workflows/`.
- Pass a configuration path or versioned configuration identifier, not arbitrary unvalidated values.
- Use run IDs and idempotency checks to prevent duplicate snapshots and reports.
- Bound retries and distinguish transient failures from data-quality failures.
- Record n8n execution metadata alongside the Python run manifest.
- Keep secrets out of workflow exports.
- For VPS hosting, use Docker Compose, persistent storage, HTTPS, strong authentication, a protected encryption key, restricted ingress, backups and an upgrade/restore runbook.
- Keep the Python CLI as the fallback if n8n is unavailable.

## 13. CLI contract

Implement at least:

```text
crypto-research validate-config --config PATH
crypto-research fetch --config PATH
crypto-research validate-data --run-id ID
crypto-research backtest --run-id ID
crypto-research report --run-id ID
crypto-research run --config PATH
crypto-research inspect-run --run-id ID
```

Commands must be composable for recovery and diagnostics. `run` may orchestrate the complete sequence, but each major stage should remain independently testable.

Exit-code guidance:

- `0`: completed successfully, including a valid “no strategy passed” result;
- `2`: invalid configuration or command usage;
- `3`: data-quality blocked;
- `4`: external provider or network failure after retry policy;
- `5`: implementation or unexpected runtime failure.

## 14. Testing requirements

### Unit tests

Cover:

- configuration validation and hashing;
- symbol mapping;
- timestamp and candle-boundary handling;
- gap and duplicate detection;
- cost calculations;
- signal timing;
- strategy outputs;
- split boundaries;
- metric calculations;
- rejection gates;
- report schema.

### Integration tests

Use recorded fixtures or a provider sandbox where available. Do not make ordinary tests depend on live network access.

Cover:

- adapter-to-canonical-schema conversion;
- raw-to-curated persistence;
- DuckDB queries over Parquet;
- a complete deterministic backtest;
- report and manifest generation;
- n8n invocation contract, if n8n is enabled.

### Negative tests

Test:

- missing bars;
- duplicate bars;
- out-of-order timestamps;
- malformed provider response;
- stale or incomplete latest candle;
- invalid symbol;
- network timeout;
- interrupted run;
- repeated retry;
- corrupted result artefact;
- n8n unavailable.

## 15. Reporting requirements

Every report must state:

- what was run and when;
- asset, venue, timeframe and lookback;
- data source and provenance;
- data-quality status;
- strategies and parameters tested;
- cost and execution assumptions;
- train, validation and out-of-sample results;
- robustness findings;
- rejected strategies and reasons;
- limitations and evidence gaps;
- a plain-English conclusion;
- whether any result is research-only and not a trading recommendation.

The report must be understandable without opening the code.

## 16. Delivery sequence

### Increment 0: technical spike

Confirm Kraken symbol coverage, historical depth, timestamps, rate limits, CCXT behaviour, `uv` compatibility, VectorBT integration and local storage. Record evidence and revise assumptions if necessary.

### Increment 1: data foundation

Build configuration, adapter, raw snapshots, canonical schema, validation, provenance and fetch commands.

### Increment 2: research engine

Build baselines, strategy protocol, initial strategies, cost model, chronological splits, metrics and report generation.

### Increment 3: robustness and operator workflow

Add sensitivity analysis, rejection gates, run manifest, result bundle, error handling, tests and the complete morning command.

### Increment 3.5: optional n8n orchestration

Add manual trigger, optional schedule, bounded retries, status capture and notifications. Prove that the Python CLI still works independently.

### Increment 4: review and future decision

Assess reproducibility and strategy credibility. Decide separately whether to proceed to paper trading. Do not move directly from backtesting to live execution.

## 17. Definition of done for the MVP

The MVP is complete only when:

- a clean machine can install and run it with `uv sync` and the committed lockfile;
- a documented command completes a public Kraken-data research run;
- no private exchange credential is required;
- raw and curated data are traceable and versioned;
- data-quality failures block or warn according to configuration;
- baseline and initial strategy results are reported consistently;
- costs, slippage and execution timing are visible;
- train, validation and out-of-sample evaluation is implemented;
- sensitivity and robustness results are present;
- failed strategies have explicit rejection reasons;
- the system can produce a valid “no strategy passed” result;
- all critical tests pass without live network dependency;
- the CLI works without n8n;
- if n8n is enabled, retries are bounded, workflows are versioned and duplicate runs are prevented;
- no code path can place live orders;
- the README and operations runbook are sufficient for another technically capable operator to run the workflow.

## 18. Future migration path

Do not begin a Rust rewrite during the MVP. First measure actual bottlenecks. If a later migration is justified:

- preserve the canonical data schema;
- preserve strategy and backtest interfaces;
- define golden datasets and expected metrics;
- compare Python and Rust outputs on identical inputs;
- migrate only profiled components;
- retain the Python CLI until the replacement is validated.

## 19. Source and evidence register

- [CCXT documentation](https://docs.ccxt.com/docs/index)
- [Kraken API documentation](https://docs.kraken.com/api/docs/)
- [Coinbase Advanced Trade documentation](https://docs.cdp.coinbase.com/advanced-trade/docs/ws-overview/)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [VectorBT documentation](https://vectorbt.dev/)
- [uv project guide](https://docs.astral.sh/uv/guides/projects/)
- [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [n8n hosting guidance](https://docs.n8n.io/deploy/host-n8n)
- [n8n Docker Compose installation](https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose.md)
- [n8n Docker and self-hosting guidance](https://docs.n8n.io/hosting/installation/docker/)
- [FCA cryptoasset guidance](https://www.fca.org.uk/firms/cryptoassets)

This specification is an implementation brief, not investment, legal or tax advice. Revalidate exchange access, API terms, fees, data availability and UK regulatory obligations before expanding beyond research.
