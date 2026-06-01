# Forex Trading Using Python Research Index

Date: 2026-05-18

Scope: Research and learning structure for building Python-based forex trading systems, from market data ingestion through backtesting, broker connectivity, strategy implementation, risk management, trader profiling, and macro context.

This is engineering and research context only. It is not trading advice.

## Drive Structure Created

- 00 Project Index and Scope
- 01 Forex Market Foundations
- 02 Data Retrieval Cleaning Processing
- 03 Python Strategy Implementation
- 04 Backtesting and Simulation
- 05 Execution Brokers FIX Interfaces
- 06 Risk Management Analysis
- 07 Trader Profile
- 08 Macro QE Central Banks Commodities
- 09 Sources and Working Notes

## Research Lanes

### Data Retrieval, Cleaning, Processing

Primary deliverable: `Data_and_Backtesting_Brief.md`

Key topics:
- Broker-linked and independent forex data APIs
- Tick, bid/ask, midpoint, and OHLCV normalization
- UTC timestamps, symbol canonicalization, deduplication, spread validation, gap detection
- Raw, clean, features, and run-output storage layers
- Parquet/DuckDB-oriented local research architecture

### Python Strategy Implementation and Backtesting

Primary deliverable: `Data_and_Backtesting_Brief.md`

Key topics:
- Backtrader, Backtesting.py, vectorbt, Zipline Reloaded, and QuantConnect LEAN
- Difference between fast vectorized research and slower event-driven simulation
- Spread, slippage, commission, latency, rollover, leverage, and margin modeling
- Reproducible backtest run records

### Broker Connectivity, FIX, Execution, and Risk

Primary deliverable: `Professional_FX_Trading_Setup_Brief.md`

Key topics:
- REST, streaming, local gateway, and professional FIX connectivity patterns
- FIX order-routing and market-data messages
- Execution quality, slippage, liquidity fragmentation, reject rates, and fill ratios
- Pre-trade, runtime, and post-trade risk controls

### Trader Profiles, Strategy Families, and Macro Context

Primary deliverable: `Trader_Profile_Strategy_Macro_Brief.md`

Key topics:
- Scalper, Day Trader, Swing Trader, Position Trader, Mechanical Trader
- Trend, mean-reversion, carry, event, commodity-linked, and mechanical systems
- Quantitative easing, central-bank intervention, and event-risk volatility regimes
- Global growth, inflation, gold, oil, and rare-earth metals as FX context

## Recommended Next Build Sequence

1. Define the trader profile questionnaire and target profile classification logic.
2. Build a data-ingestion prototype with one free historical source and one broker-style API.
3. Store raw and cleaned datasets separately, preferably in partitioned Parquet.
4. Implement one simple strategy family twice: vectorized first, then event-driven.
5. Add realistic execution assumptions before evaluating performance.
6. Add risk limits outside the strategy code path.
7. Create a macro-event and central-bank calendar layer before testing event-sensitive strategies.

## Initial Python Package Shape

```text
forex_lab/
  data/
    ingest.py
    normalize.py
    validate.py
    resample.py
  features/
    indicators.py
    macro.py
    regimes.py
  strategies/
    base.py
    trend.py
    mean_reversion.py
    carry.py
  backtesting/
    vectorized.py
    event_driven.py
    costs.py
    reporting.py
  execution/
    broker_adapter.py
    fix_adapter.py
    order_state.py
  risk/
    limits.py
    sizing.py
    kill_switch.py
  research/
    trader_profile.py
    experiments.py
```

## Immediate Research Gaps To Fill Next

- Broker comparison by jurisdiction, API capability, demo environment quality, and historical-data access.
- Specific trader-profile questionnaire with scoring weights.
- Starter notebook for data ingestion and feature generation.
- Backtest template with spread, slippage, financing, and margin assumptions exposed as config.
- Source pack for macro calendars, central-bank statements, rates, gold, oil, and rare-earth market data.

