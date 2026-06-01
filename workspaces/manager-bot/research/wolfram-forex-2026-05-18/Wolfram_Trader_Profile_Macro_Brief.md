# Wolfram Trader Profile and Macro Context Brief

This is research context only, not trading advice.

## Trader Profiles In A Wolfram Workflow

Scalper:
- Wolfram role: post-trade analytics, spread/latency diagnostics, simulation, and reporting.
- Caution: live scalping execution should not depend on notebook latency or manual notebook state.
- Data needs: tick/quote data, bid/ask spread, session liquidity, latency logs.

Day Trader:
- Wolfram role: intraday dashboards, indicators, economic-calendar overlays, session studies, and end-of-day reports.
- Data needs: 1-minute to 15-minute bars, macro event timestamps, spread/volatility regimes.

Swing Trader:
- Wolfram role: daily/4-hour time-series analysis, moving-average/trend/regime models, and walk-forward reports.
- Data needs: daily and intraday bars, rates, inflation, growth, central-bank signals.

Position Trader:
- Wolfram role: macro notebooks, cross-country comparisons, interest-rate/inflation/growth dashboards, and scenario analysis.
- Data needs: daily/weekly FX, policy rates, CPI, GDP, trade balances, commodities.

Mechanical Trader:
- Wolfram role: fully specified rules, parameter sweeps, backtest reports, risk dashboards, and model documentation.
- Data needs: clean point-in-time datasets, explicit costs, reproducible configs, testable package code.

## Wolfram Profile Questionnaire Pattern

The profile can be implemented as a notebook form or `FormFunction` that scores:

- preferred holding period
- tolerance for frequent decisions
- comfort with code-only execution
- need for discretion versus fully specified rules
- available monitoring time
- tolerance for overnight/weekend exposure
- sensitivity to transaction costs
- interest in macro research

Output should classify the user into one primary profile and one secondary profile, then map that to recommended notebook templates and data frequencies.

## Macro, QE, Central Banks, and Commodities

Wolfram is well suited to macro/market context work because notebooks combine data, code, visualization, text, and reports.

Recommended notebooks:

- `CentralBankPolicy.nb`: policy rates, statements, balance-sheet indicators, press-conference dates.
- `InflationGrowthDashboard.nb`: CPI, GDP, employment, PMIs, and surprises.
- `CommodityFXContext.nb`: oil, gold, industrial metals, rare-earth supply-chain notes, and commodity-linked currencies.
- `VolatilityRegimes.nb`: realized volatility, event windows, spread widening, central-bank decision windows.
- `ScenarioLibrary.nb`: inflation shock, growth slowdown, oil spike, gold rally, intervention shock, risk-off stress.

QE and central-bank intervention should be treated as regime-changing events, not ordinary price noise. In Wolfram terms, event windows should be explicit objects or annotated time intervals joined to FX time series before modeling.

## Strategy Context

Trend following:
- Wolfram implementation: moving averages, channel breakout logic, `TimeSeries` features, `TradingChart` diagnostics.

Mean reversion:
- Wolfram implementation: z-scores, rolling mean/std with `MovingMap`, volatility filters, range/regime classification.

Carry/rates:
- Wolfram implementation: rates and inflation panels, currency pair ranking, scenario tables, exposure reports.

Macro event:
- Wolfram implementation: event-window studies, surprise variables, volatility before/after central-bank or CPI releases.

Commodity-linked FX:
- Wolfram implementation: gold/oil/commodity series joined to FX pairs, rolling beta/correlation, scenario notebooks.

Mechanical systems:
- Wolfram implementation: package-defined rules, `.wlt` tests, parameter sweeps, walk-forward reports, and risk dashboards.

## Sources

1. Wolfram `FormFunction`: <https://reference.wolfram.com/language/ref/FormFunction.html>
2. Wolfram `Dataset`: <https://reference.wolfram.com/language/ref/Dataset.html>
3. Wolfram `TimeSeries`: <https://reference.wolfram.com/language/ref/TimeSeries.html>
4. Wolfram `TradingChart`: <https://reference.wolfram.com/language/ref/TradingChart.html>
5. Wolfram `DateListPlot`: <https://reference.wolfram.com/language/ref/DateListPlot.html>
6. BIS, Triennial Central Bank Survey of FX turnover: <https://www.bis.org/statistics/rpfx22_fx.htm>
7. Federal Reserve, balance sheet and open market operations: <https://www.federalreserve.gov/monetarypolicy/bst_openmarketops.htm>
8. ECB asset purchase programmes: <https://www.ecb.europa.eu/mopo/implement/app/html/index.en.html>
9. IMF World Economic Outlook: <https://www.imf.org/en/Publications/WEO>
10. World Bank Commodity Markets: <https://www.worldbank.org/en/research/commodity-markets>
11. EIA oil prices and outlook: <https://www.eia.gov/energyexplained/oil-and-petroleum-products/prices-and-outlook.php>
12. USGS Rare Earths mineral commodity summary: <https://pubs.usgs.gov/periodicals/mcs2024/mcs2024-rare-earths.pdf>

