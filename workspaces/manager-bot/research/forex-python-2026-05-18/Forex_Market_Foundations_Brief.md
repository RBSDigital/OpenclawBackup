# Forex Market Foundations Brief

This is learning and research context only, not trading advice.

## What The FX Market Is

The foreign exchange market is the global market for exchanging currencies. It is decentralized and mostly over-the-counter rather than concentrated on one exchange. Trading happens through banks, dealers, brokers, electronic communication networks, institutional platforms, and retail brokers.

The Bank for International Settlements' triennial survey is the main high-level reference for global FX market size, structure, currency share, and instrument turnover.

## Core Instruments

- Spot FX: exchange of one currency for another, usually quoted as a currency pair such as EUR/USD.
- Forwards: agreements to exchange currencies at a future date and agreed rate.
- FX swaps: paired spot and forward transactions, widely used by institutions for funding and hedging.
- Options: contracts giving the right, but not the obligation, to buy or sell currency at a specified rate.
- CFDs/retail margin FX: broker-provided leveraged exposure; mechanics, protections, and risks vary by jurisdiction.

## How Currency Pairs Work

- Base currency: first currency in the pair, for example EUR in EUR/USD.
- Quote currency: second currency in the pair, for example USD in EUR/USD.
- Bid: price at which the market/broker buys the base currency from the trader.
- Ask/offer: price at which the market/broker sells the base currency to the trader.
- Spread: ask minus bid; a direct transaction cost.
- Pip: common minimum price increment convention, often 0.0001 for many major pairs and 0.01 for JPY pairs, though brokers may quote fractional pips.

For Python systems, pair metadata should be explicit: quote precision, pip location, minimum trade size, margin requirement, trading hours, and rollover/financing rules.

## Market Participants

- Central banks: monetary policy, reserves, intervention, financial stability.
- Commercial banks and dealers: market-making, liquidity, client flow, hedging.
- Asset managers and hedge funds: portfolio hedging, macro views, systematic strategies.
- Corporates: trade flows, international revenues/costs, hedging.
- Brokers and platforms: retail/professional access, execution, margin, market data.
- Retail traders: usually via margin FX, CFDs, or broker APIs depending on jurisdiction.

## Main Drivers

- Interest-rate differentials and expected monetary-policy paths.
- Inflation, growth, employment, trade balances, fiscal credibility, and debt sustainability.
- Risk sentiment and safe-haven flows.
- Commodity exposure, especially oil and gold for certain currencies.
- Central-bank intervention and reserve management.
- Political and geopolitical shocks.
- Liquidity conditions, funding stress, and market positioning.

## Trading Sessions and Liquidity

FX trades around the clock during the global business week, but liquidity is not constant. London and New York overlap tends to be more liquid for many major pairs; Asia-Pacific sessions matter heavily for JPY, AUD, NZD, CNH, and regional risk. Spreads can widen around daily rollover, holidays, major data releases, and market stress.

For backtesting, session filters and time-of-day spread models matter. A strategy that looks profitable on midpoint daily candles may fail when tested with bid/ask, spread widening, rollover, and event windows.

## Why This Matters For Python Algorithms

A usable Python FX research system should model:
- executable bid/ask prices, not only midpoint prices;
- time-zone and session effects;
- spread and slippage;
- broker-specific lot size, precision, margin, and rollover;
- macro-event calendars and central-bank decision windows;
- reproducible data versions and backtest configurations.

## Sources

1. BIS, Triennial Central Bank Survey of FX turnover: <https://www.bis.org/statistics/rpfx22_fx.htm>
2. BIS, OTC foreign exchange turnover in April 2022: <https://www.bis.org/statistics/rpfx22_fx.pdf>
3. BIS, FX market structure and recent developments: <https://www.bis.org/publ/qtrpdf/r_qt2209x.htm>
4. CFTC, Retail foreign exchange transactions: <https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/fraudadv_forex.html>
5. OANDA v20 instruments and pricing API overview: <https://developer.oanda.com/rest-live-v20/introduction/>
6. Federal Reserve, monetary policy and open market operations: <https://www.federalreserve.gov/monetarypolicy/openmarket.htm>

