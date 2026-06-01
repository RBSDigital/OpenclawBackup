# Wolfram Forex Market Foundations Brief

This is learning and research context only, not trading advice.

## FX Market Basics

The foreign exchange market is decentralized and mostly over-the-counter rather than concentrated on one exchange. Trading occurs through banks, dealers, brokers, electronic platforms, institutional venues, and retail brokers.

The main instruments are spot FX, forwards, FX swaps, options, and retail margin/CFD-style products depending on jurisdiction. For Wolfram research, the most important distinction is whether the dataset represents midpoint history, bid/ask quotes, executable broker prices, or derived/aggregated bars.

## Currency Pair Data Model

A Wolfram research dataset should keep these fields explicit:

- pair, for example `"EURUSD"`
- base currency and quote currency
- vendor symbol
- vendor timestamp
- normalized UTC timestamp
- bid
- ask
- spread
- mid
- source
- data pull timestamp
- sampling interval

Do not collapse bid/ask into midpoint unless the analysis explicitly uses midpoint. Strategy backtests should know whether they are using executable prices, indicative prices, or broad historical reference prices.

## Wolfram Representation

Use `Dataset` for raw and normalized rows. Use `TimeSeries` for single-pair numeric fields, such as EUR/USD mid or spread. Use `TemporalData` or associations of `TimeSeries` for multi-pair panels.

Typical mapping:

- raw vendor export: `Dataset`
- cleaned bid series: `TimeSeries`
- cleaned ask series: `TimeSeries`
- spread series: `TimeSeries`
- multi-pair panel: `Association[pair -> <|"Bid" -> ts, "Ask" -> ts|>]`
- reporting view: `Dataset` plus charts/notebook text

## Session and Liquidity Notes

FX trades around the clock during the global business week, but liquidity is not constant. London/New York overlap is often more liquid for major pairs; Asia-Pacific matters heavily for JPY, AUD, NZD, CNH, and regional risk. Spreads can widen around daily rollover, holidays, major data releases, and market stress.

For Wolfram backtesting, use explicit time filters and event windows. A notebook chart that looks clean on daily midpoints can hide spread widening, slippage, rollover, and weekend gaps.

## Why It Matters For Wolfram Research

Wolfram is strong for notebooks, visualization, symbolic structure, time-series analysis, and reproducible reports. It is less appropriate as the sole owner of low-latency live trading state. The practical split is:

- Wolfram: research, analysis, backtest reports, scenario notebooks, model monitoring.
- External services: market-data ingestion, broker/FIX connectivity, order lifecycle, hard risk gates, durable audit logs.

## Sources

1. BIS, Triennial Central Bank Survey of FX turnover: <https://www.bis.org/statistics/rpfx22_fx.htm>
2. BIS, OTC foreign exchange turnover in April 2022: <https://www.bis.org/statistics/rpfx22_fx.pdf>
3. BIS, FX market structure and recent developments: <https://www.bis.org/publ/qtrpdf/r_qt2209x.htm>
4. CFTC, retail foreign exchange advisory: <https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/fraudadv_forex.html>
5. Wolfram `FinancialData`: <https://reference.wolfram.com/language/ref/FinancialData.html>
6. Wolfram `TimeSeries`: <https://reference.wolfram.com/language/ref/TimeSeries.html>
7. Wolfram `Dataset`: <https://reference.wolfram.com/language/ref/Dataset.html>

