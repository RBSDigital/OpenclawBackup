# Forex Trading Using Python: Data and Backtesting Brief

This is engineering and research context only, not trading advice.

## Data Sources and APIs

- OANDA v20 REST API: practical broker-linked source for live/practice pricing, candles, accounts, and order simulation workflows. Useful when the backtest needs to line up with a possible execution venue. [1]
- Dukascopy historical data export: widely used free historical FX source, especially for tick-level bid/ask research and offline dataset building. [2]
- Alpha Vantage FX endpoints: accessible API for currency exchange rates and FX time series, with free/premium limits depending on endpoint and usage. [3]
- Massive / Polygon Forex API: paid market data API with forex aggregates, quotes, and reference endpoints; useful for production ingestion with predictable API contracts. [4]
- Twelve Data Forex API: accessible REST API option for time series and FX symbols; useful for prototyping and low-volume research. [5]

## Retrieval, Cleaning, and Processing Pipeline

- Ingest: pull raw vendor responses with `requests` or `httpx`; save untouched JSON, CSV, or binary payloads first.
- Normalize: convert timestamps to UTC, enforce canonical symbols like `EURUSD`, store source symbol separately, and standardize columns: `timestamp`, `symbol`, `bid`, `ask`, `mid`, `open`, `high`, `low`, `close`, `volume`, `source`.
- Deduplicate: remove exact duplicate ticks/bars; keep deterministic conflict rules by `source_priority`, `received_at`, and vendor revision if available.
- Validate: reject negative prices, crossed quotes unless source explains them, impossible spreads, non-monotonic timestamps, and large gaps outside known market closures.
- Resample: generate bars from tick bid/ask, not only mid; store bid/ask OHLC separately if the strategy uses executable prices.
- Feature build: compute features in batch jobs from cleaned data only; version feature definitions so backtests can be reproduced.
- Persist: store immutable raw data plus cleaned Parquet datasets partitioned by `asset_class=sfx/symbol/year/month/day`; query with DuckDB, Polars, or Spark as scale requires. Apache Parquet is designed as a columnar storage format, and DuckDB has direct Parquet query support. [6][7]

## Backtesting and Simulation Libraries

- Backtrader: mature event-driven framework with data feeds, broker abstraction, commissions, and slippage support; good for order lifecycle testing and custom execution models. [8]
- Backtesting.py: lightweight Python framework for fast strategy iteration; supports commissions and simple strategy workflows. [9]
- vectorbt: vectorized, pandas/NumPy/Numba-oriented library for large parameter sweeps and portfolio research; better for signal research than highly detailed microstructure simulation. [10]
- Zipline Reloaded: event-driven backtesting framework; historically equity-focused, but useful as a reference architecture for bundles, calendars, pipelines, and order simulation. [11]
- QuantConnect LEAN: full algorithmic trading engine with explicit reality-modeling concepts including fees, fills, slippage, buying power, and portfolio models. Useful as a design reference even if running locally/custom. [12]

## Practical Architecture

Storage layers:
- `raw`: immutable vendor payloads.
- `clean`: normalized tick/bar Parquet.
- `features`: point-in-time-safe feature tables.
- `runs`: backtest configs, code version, data snapshot hash, metrics, orders, fills, equity curves.

Data model:
- Tick data: `timestamp`, `symbol`, `bid`, `ask`, `bid_size`, `ask_size`, `source`.
- Bar data: maintain `bid_ohlc`, `ask_ohlc`, and `mid_ohlc`; do not rely only on midpoint prices for execution.

Execution realism:
- Model buys at ask and sells at bid.
- Include variable spread by time of day and event windows.
- Add commissions, financing/swap/rollover, leverage, margin constraints, and minimum lot sizes.
- Simulate latency by delaying signal timestamp to order submission and fill timestamp.
- Use order-type-specific fills: market, limit, stop, partial fills, rejection, and slippage.

Backtest discipline:
- Use point-in-time features only.
- Separate train, validation, and test periods.
- Record every run's config, data version, git SHA, random seed, and dependency lockfile.
- Compare a fast vectorized research pass against a slower event-driven simulation before trusting results.

## Sources

1. OANDA v20 REST API: <https://developer.oanda.com/rest-live-v20/introduction/>
2. Dukascopy historical FX data export: <https://www.dukascopy.com/swiss/english/marketwatch/historical/>
3. Alpha Vantage FX documentation: <https://www.alphavantage.co/documentation/>
4. Massive / Polygon Forex API docs: <https://massive.com/docs/forex/getting-started>
5. Twelve Data Forex API docs: <https://twelvedata.com/docs#forex>
6. Apache Parquet docs: <https://parquet.apache.org/docs/>
7. DuckDB Parquet docs: <https://duckdb.org/docs/stable/data/parquet/overview>
8. Backtrader documentation: <https://www.backtrader.com/docu/>
9. Backtesting.py documentation: <https://kernc.github.io/backtesting.py/>
10. vectorbt documentation: <https://vectorbt.dev/>
11. Zipline documentation: <https://www.zipline.io/>
12. QuantConnect reality modeling docs: <https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/key-concepts>

