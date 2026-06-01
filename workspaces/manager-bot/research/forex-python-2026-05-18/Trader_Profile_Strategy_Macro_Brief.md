# Forex Strategy, Trader Profile, and Macro Context Brief

This is research context only, not trading advice.

## Trader Profiles

| Profile | Holding Period | Decision Criteria | Typical Data Needs |
|---|---:|---|---|
| Scalper | Seconds to minutes | Spread, tick momentum, liquidity, session volatility, order-flow imbalance | Tick/1m OHLCV, spreads, latency metrics |
| Day Trader | Minutes to same day | Intraday trend, range breaks, news calendar, VWAP/mean reversion, session open/close behavior | 1m-15m OHLCV, economic calendar, volatility |
| Swing Trader | Days to weeks | Trend continuation, pullbacks, support/resistance, rate-differential shifts, macro surprises | 4h/daily OHLCV, indicators, rates, macro data |
| Position Trader | Weeks to months | Monetary policy divergence, inflation/growth trends, commodity exposure, external balances | Daily/weekly prices, rates, CPI/GDP, commodities |
| Mechanical Trader | Any | Fully specified rules, backtestable signals, execution constraints, risk limits | Clean historical data, signal engine, backtester |

## Strategy Families and Python Module Translation

Trend following:
- Logic: moving-average crossovers, Donchian channels, breakout confirmation.
- Python modules: `data_loader.py`, `indicators.py`, `signals_trend.py`, `backtest.py`.

Mean reversion:
- Logic: z-scores, Bollinger Bands, RSI extremes, range-bound regime filters.
- Python modules: `features_stat.py`, `signals_reversion.py`, `regime.py`.

Carry/rates differential:
- Logic: compare policy rates, forward points, real yield differentials, central-bank bias.
- Python modules: `macro_rates.py`, `carry_model.py`, `calendar_events.py`.

News/macro event trading:
- Logic: CPI, jobs, GDP, central-bank decisions, surprise versus consensus.
- Python modules: `event_calendar.py`, `macro_surprises.py`, `volatility_filter.py`.

Commodity-linked FX:
- Logic: oil-sensitive currencies, gold risk hedging, metals demand, terms-of-trade shifts.
- Python modules: `commodities.py`, `fx_commodity_beta.py`, `macro_dashboard.py`.

Mechanical portfolio systems:
- Logic: combine signals with fixed position sizing, stop rules, drawdown caps, walk-forward validation.
- Python modules: `strategy_base.py`, `portfolio.py`, `risk.py`, `execution.py`, `reports.py`.

## Central Bank Intervention, QE, and Volatility

Central-bank balance-sheet expansion and asset purchases can lower longer-term yields, compress risk premia, weaken or stabilize a currency depending on relative policy stance, and push investors into higher-yielding assets. The Federal Reserve and ECB both document asset-purchase and balance-sheet tools as part of monetary-policy implementation.

Direct FX intervention can produce sharp short-term moves, especially when it surprises markets or aligns with broader monetary policy. However, intervention durability depends on scale, credibility, coordination, reserve capacity, and whether it changes expected interest-rate paths.

Volatility spikes often occur around:
- central-bank rate decisions and press conferences;
- surprise inflation or labor-market data;
- emergency liquidity operations;
- geopolitical shocks;
- commodity supply disruptions;
- sudden changes in market expectations for QE, QT, or intervention.

For system design, these events should be modeled as regime changes, not ordinary price noise. A Python stack should separate normal signal generation from `event_risk.py`, `liquidity_filter.py`, and `volatility_regime.py`.

## Macro Commodities In FX Analysis

- Global growth: stronger global growth can support pro-cyclical and commodity-linked currencies; weak growth can benefit reserve or funding currencies.
- Inflation: higher inflation can support a currency if it raises expected policy rates, but weaken it if real yields fall or credibility erodes.
- Gold: often functions as a hedge against currency debasement, geopolitical stress, and real-yield declines; gold-linked analysis is relevant for USD, CHF, AUD, and reserve-allocation narratives.
- Oil: oil importers and exporters can be affected differently through trade balances, inflation, fiscal revenues, and current-account pressure.
- Rare-earth metals: rare earths matter through industrial policy, supply-chain security, China exposure, defense technology, EVs, and clean-energy demand. They are less directly traded in FX than oil or gold, but can affect currencies through trade, strategic-resource policy, and manufacturing competitiveness.

## Sources

1. BIS, Triennial Central Bank Survey of FX turnover: <https://www.bis.org/statistics/rpfx22_fx.htm>
2. BIS, FX market structure and policy context: <https://www.bis.org/publ/qtrpdf/r_qt2209x.htm>
3. Federal Reserve, balance sheet and open market operations: <https://www.federalreserve.gov/monetarypolicy/bst_openmarketops.htm>
4. Federal Reserve, central-bank balance sheets and long-term rates: <https://www.federalreserve.gov/econres/notes/feds-notes/central-bank-balance-sheets-and-long-term-interest-rates-20200714.html>
5. ECB, asset purchase programmes: <https://www.ecb.europa.eu/mopo/implement/app/html/index.en.html>
6. IMF, World Economic Outlook: <https://www.imf.org/en/Publications/WEO>
7. World Bank, Commodity Markets: <https://www.worldbank.org/en/research/commodity-markets>
8. EIA, oil prices and outlook: <https://www.eia.gov/energyexplained/oil-and-petroleum-products/prices-and-outlook.php>
9. World Gold Council, gold and currencies: <https://www.gold.org/goldhub/research/gold-and-currencies-hedging-fx-risk>
10. USGS, Rare Earths mineral commodity summary: <https://pubs.usgs.gov/periodicals/mcs2024/mcs2024-rare-earths.pdf>

